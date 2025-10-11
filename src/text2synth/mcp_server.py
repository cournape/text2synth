import inspect
import io
import logging
import textwrap
import time

from enum import Enum
from typing import Callable, Optional, get_origin

import mido

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

from text2synth.state import JU06AState


LOGGER = logging.getLogger(__name__)


# 1-1 factory sound for 106 mode
INIT_106 = """\
LFO RATE        (30);
LFO DELAY TIME  (59);
LFO WAVE        (0);
LFO TRIG        (0);
OSC RANGE       (0);
OSC LFO MOD     (0);
PWM             (253);
PWM SOURCE      (0);
SQR SW          (0);
SAW SW          (1);
SUB LEVEL       (0);
NOISE LEVEL     (0);
SUB SW          (0);
HPF             (41);
CUTOFF          (102);
RESONANCE       (17);
ENV POLARITY    (1);
ENV MOD         (100);
FLT LFO MOD     (0);
FLT KEY FOLLOW  (194);
AMP MODE        (1);
AMP LEVEL       (255);
ATTACK          (32);
DECAY           (110);
SUSTAIN         (119);
RELEASE         (60);
CHORUS SW       (1);
DELAY LEVEL     (8);
DELAY TIME      (11);
DELAY FEEDBACK  (8);
DELAY SW        (0);
PORTA SW        (0);
PORTA TIME      (100);
ASSIGN MODE     (0);
BEND RANGE      (2);
TEMPO SYNC      (0);
PATCH_NAME(Brass           );
"""


STATE = JU06AState.from_file(io.StringIO(INIT_106))
DEFAULT_MIDI_OUT = "USB MIDI Interface"


server = FastMCP('Text2Synth MCP Server')


def apply_state_to_synth(state):
    outport_name = DEFAULT_MIDI_OUT
    with mido.open_output(outport_name) as outport:
        LOGGER.debug("Ready to use MIDI port %s", outport_name)
        for msg in state.to_cc_messages():
            outport.send(msg)
            # Sleeping a bit to avoid flooding the MIDI connection
            time.sleep(0.001)


def create_function_from_model(model_class: type[BaseModel], wrapped_func: Callable):
    """
    Function factory from a Pydantic model. Created function can be then
    exposed as MCP tools through FastMCP with metadata inferred from the model
    class.

    The created function will have a signature that is kw-only, one
    keyword per field. Critically, the generated function will have a docstring
    and __signature__ that maps the fields, type and description for the
    pydantic class. This exposes the right info when exposing the function as
    an MCP tool.

    Parameters
    ----------
    model_class : type[BaseModel]
        The Pydantic model class to generate a function from
    wrapped_func : Callable
        Name for the generated function (defaults to model class name lowercase)

    Returns
    -------
    callable
        A function with signature matching the model's fields
    """
    func_name = wrapped_func.__name__

    # Get model fields
    fields = model_class.model_fields

    # Build parameter list for signature
    params = []
    param_docs = []

    for field_name, field_info in fields.items():
        # Get the annotation - make it Optional
        annotation = field_info.annotation
        optional_annotation = Optional[annotation]
        
        # All parameters default to None
        param = inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=None,
            annotation=optional_annotation
        )
        params.append(param)
        
        description = field_info.description or "<No description provided>"
        type_str = annotation.__name__ if hasattr(annotation, '__name__') else str(annotation)
        
        constraints = []
        
        # Check if it's an Enum
        if inspect.isclass(annotation) and issubclass(annotation, Enum):
            enum_values = [f"'{e.value}'" if isinstance(e.value, str) else str(e.value) 
                          for e in annotation]
            constraints.append(f"Possible values: {', '.join(enum_values)}")
        
        # Check for numeric constraints (ge, le, gt, lt)
        elif annotation in (int, float) or (get_origin(annotation) in (int, float)):
            range_parts = {}

            for m in field_info.metadata:
                if hasattr(m, "le"):
                    range_parts[1] = m.le
                if hasattr(m, "ge"):
                    range_parts[0] = m.ge

            if range_parts:
                constraints.append(f"Range: {', '.join(str(range_parts[k]) for k in (0, 1))}")
        
        # Format the parameter documentation
        param_doc = f"    {field_name} : {type_str}, optional\n        {description}"
        if constraints:
            param_doc += f"\n        {'; '.join(constraints)}"
        
        param_docs.append(param_doc)

    docstring = textwrap.dedent(f"""\
    Function generated from {model_class.__name__} model.

    Parameters
    ----------
{chr(10).join(param_docs)}
    """)

    def generated_func(**kwargs) -> None:
        updates = {k: v for k, v in kwargs.items() if v is not None}
        wrapped_func(**updates)

    # Note: None is for explicit -> None, not for no annotation
    sig = inspect.Signature(params, return_annotation=None)

    annotations = {}
    for name, param in sig.parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            annotations[name] = param.annotation
    annotations['return'] = None

    generated_func.__annotations__ = annotations
    generated_func.__signature__ = sig
    generated_func.__name__ = func_name
    generated_func.__doc__ = docstring

    return generated_func


def update_synth_state(**kw):
    for k, v in kw.items():
        setattr(STATE, k, v)
    apply_state_to_synth(STATE)


update_synth = create_function_from_model(JU06AState, update_synth_state)
update_synth = server.tool()(update_synth)


@server.tool()
def reset() -> None:
    """Reset the state to initial state"""
    global STATE
    STATE = JU06AState.from_file(io.StringIO(INIT_106))
    apply_state_to_synth(STATE)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server.run()
