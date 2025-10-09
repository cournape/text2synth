#!/usr/bin/env python3
import argparse
import asyncio
import logging
import sys
import textwrap
import time

from pathlib import Path

import mido

from pydantic_ai import Agent

from text2synth.state import JU06AState


DEFAULT_MIDI_IN = DEFAULT_MIDI_OUT = "USB MIDI Interface"
LOGGER = logging.getLogger(__name__)

DEFAULT_LLM_MODEL = "anthropic:claude-sonnet-4-5"


def list_ports_cli(args):
    print("MIDI Input Ports:")
    for name in mido.get_input_names():
        print("  ", name)

    print("\nMIDI Output Ports:")
    for name in mido.get_output_names():
        print("  ", name)


def control_change_cli(args):
    outport_name = args.midi_out
    number = args.cc_number
    value = args.cc_value

    LOGGER.debug("Sending CC %d with value %d", number, value)

    with mido.open_output(outport_name) as outport:
        LOGGER.debug("Ready to use port")

        msg = mido.Message('control_change', control=number, value=value)
        outport.send(msg)


def analyze_patch_ranges_cli(args):
    """
    Recursively analyze all .PRM patch files to find min/max ranges for each parameter.

    Parameters
    ----------
    directory : Path
        Directory to search for .PRM files (searches recursively)

    Returns
    -------
    Dict[str, Tuple[int, int]]
        Dictionary mapping attribute names to (min, max) tuples for all numerical attributes
    """
    path = args.path

    # Dictionary to track min/max for each attribute
    ranges = {}

    # Recursively find all .PRM files
    prn_files = list(Path(path).rglob("*.PRM"))

    if not prn_files:
        print(f"Warning: No .PRM files found in {path}")
        return ranges

    print(f"Found {len(prn_files)} .PRM files")

    for prn_file in prn_files:
        try:
            patch = JU06AState.from_path(str(prn_file))

            for attr_name in JU06AState.model_fields:
                value = getattr(patch, attr_name)

                # Skip non-integer attributes (like patch_name)
                if not isinstance(value, int):
                    continue

                # Update min/max for this attribute
                if attr_name not in ranges:
                    ranges[attr_name] = (value, value)
                else:
                    current_min, current_max = ranges[attr_name]
                    ranges[attr_name] = (min(current_min, value), max(current_max, value))

        except Exception as e:
            print(f"Error processing {prn_file}: {e}")
            continue

    print("\nParameter Ranges:")
    print("-" * 50)

    if args.show_double_only:
        for attr_name, (min_val, max_val) in sorted(ranges.items()):
            if max_val > 128 and max_val <= 255:
                print(attr_name)
    else:
        for attr_name, (min_val, max_val) in sorted(ranges.items()):
            print(f"{attr_name:20s}: {min_val:3d} - {max_val:3d}")


def program_change_cli(args):
    outport_name = args.midi_out
    program = args.program
    LOGGER.info("Changing program to %d", program)

    assert program >= 1

    with mido.open_output(outport_name) as outport:
        LOGGER.debug("Ready to use port")

        msg = mido.Message('program_change', program=program-1)
        outport.send(msg)


def apply_state_to_synth(state, outport_name):
    with mido.open_output(outport_name) as outport:
        LOGGER.debug("Ready to use MIDI port %s", outport_name)
        for msg in state.to_cc_messages():
            outport.send(msg)
            # Sleeping a bit to avoid flooding the MIDI connection
            time.sleep(0.001)


def send_patch_cli(args):
    outport_name = args.midi_out
    path = args.path
    LOGGER.info("Applying PRM file %s", path)

    state = JU06AState.from_path(path)
    apply_state_to_synth(state, outport_name)


def load_patches(patch_directory: str, max_examples=None) -> str:
    """
    Load patches in their original text format.

    Parameters
    ----------
    patch_directory : str
        Directory containing .PRM patch files
    max_examples : int
        Maximum number of examples to include

    Returns
    -------
    str
        Concatenated original patch files
    """

    patches = []
    paths = list(Path(patch_directory).rglob("*.PRM"))[:max_examples]
    print(f"Loading {len(paths)} patches")

    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                patches.append(f"=== {path.name} ===\n{content}\n")

        except Exception:
            continue

    return "\n".join(patches)


async def text2patch_cmd(agent, description, outport_name, output_path="test-patch.prm", patch_name="TEST PATCH"):
    result = await agent.run(description)

    state = result.output
    state.to_path(output_path, patch_name)

    LOGGER.debug("Applying to synth")
    apply_state_to_synth(state, "USB MIDI Interface")


def text2patch_cli(args):
    outport_name = args.midi_out
    patches_path = args.patches_path
    max_patches = args.max_patches
    description = args.description
    llm_model = args.llm_model

    if patches_path is not None:
        patches = load_patches(patches_path, max_patches)
    else:
        patches = ""

    # Create agent
    agent = Agent(
        llm_model,
        output_type=JU06AState,
        system_prompt=textwrap.dedent(f"""You are an expert sound designer for the Roland JU-06A synthesizer.

        Create synthesizer patches based on user descriptions. Consider:
        - Filter cutoff and resonance for brightness and character
        - Envelope (ADSR) for shaping the sound over time
        - LFO for modulation effects
        - Oscillator settings for tone color
        - Effects like chorus and delay for depth

        Here are example patches from real JU-06A presets to learn from:

        {patches}

        Generate creative, musically useful patches that match the user's description.""",
        )
    )
    LOGGER.debug("Agent %s is created", agent)

    asyncio.run(
        text2patch_cmd(agent, description, outport_name)
    )


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s:%(module)s.%(funcName)s: %(message)s")

    parser = argparse.ArgumentParser(description="Simple MIDI CLI")
    parser.add_argument("--midi-in", type=str, default=DEFAULT_MIDI_IN,
                        help="MIDI input device")
    parser.add_argument("--midi-out", type=str, default=DEFAULT_MIDI_OUT,
                        help="MIDI output device")

    subparsers = parser.add_subparsers(dest="command", required=True)

    pc_parser = subparsers.add_parser("program-change", aliases=["pc"],
                                      help="Send a Program change")
    pc_parser.add_argument("program", type=int, help="Program number")
    pc_parser.add_argument("--channel", type=int, default=1,
                           help="MIDI channel (default: 1)")
    pc_parser.set_defaults(func=program_change_cli)

    send_patch_parser = subparsers.add_parser("send-patch",
                                              help="Apply the given patch file to the synth through MIDI")
    send_patch_parser.add_argument("path", type=str, help="Path to the PRM file")
    send_patch_parser.set_defaults(func=send_patch_cli)

    cc_parser = subparsers.add_parser("control-change", aliases=["cc"],
                                      help="Send a MIDI control change message")
    cc_parser.add_argument("cc_number", type=int, help="Control change number")
    cc_parser.add_argument("cc_value", type=int, help="Control change value")
    cc_parser.add_argument("--channel", type=int, default=1,
                           help="MIDI channel (default: 1)")
    cc_parser.set_defaults(func=control_change_cli)

    stats_parser = subparsers.add_parser("stats",
                                      help="Parse patches to find range statistics")
    stats_parser.add_argument("path", type=str, help="Directory to recursively walk")
    stats_parser.add_argument("--show-double-only", action="store_true",
                              default=False,
                              help="If given, only print CC that go beyond 127")
    stats_parser.set_defaults(func=analyze_patch_ranges_cli)

    list_ports_parser = subparsers.add_parser("list-ports",
                                      help="list ports")
    list_ports_parser.set_defaults(func=list_ports_cli)

    text2patch_parser = subparsers.add_parser("text2patch", aliases=["t2p"],
                                      help="Create a new patch from description and apply it to the synth")
    text2patch_parser.add_argument("description", type=str, help="Patch description")
    text2patch_parser.add_argument("--max-patches", type=int, help="Max patches to load")
    text2patch_parser.add_argument("--patches-path", type=str, help="Where to look for patches")
    text2patch_parser.add_argument("--llm-model", type=str, help="The LLM to use", default=DEFAULT_LLM_MODEL)
    text2patch_parser.set_defaults(func=text2patch_cli)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        print("No operation implemented for this command yet.")
        sys.exit(-1)

if __name__ == "__main__":
    main()
