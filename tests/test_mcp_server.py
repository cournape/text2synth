import inspect
import textwrap

from typing import Optional

from pydantic import BaseModel, Field

from text2synth.mcp_server import create_function_from_model


class TestToolFactory:
    def test_str(self):
        # Given
        class SimpleModel(BaseModel):
            a: str

        def func_ref(a: Optional[str] = None) -> None:
            pass

        docstring_ref = textwrap.dedent("""\
        Function generated from SimpleModel model.

        Parameters
        ----------
        a : str, optional
            <No description provided>
        """)
        # When
        def dummy(**kw): pass
        func = create_function_from_model(SimpleModel, dummy)

        # Then
        assert func.__doc__ == docstring_ref
        assert func.__annotations__ == {"return": None}
        assert func.__signature__ == inspect.signature(func_ref)

    def test_simple(self):
        # Given
        class SimpleModel(BaseModel):
            a: int = Field(description="first arg") 
            b: int = Field(description="second arg") 

        def func_ref(a: Optional[int] = None, b : Optional[int] = None) -> None:
            pass

        docstring_ref = textwrap.dedent("""\
        Function generated from SimpleModel model.

        Parameters
        ----------
        a : int, optional
            first arg
        b : int, optional
            second arg
        """)
        # When
        def dummy(**kw): pass
        func = create_function_from_model(SimpleModel, dummy)

        # Then
        assert func.__doc__ == docstring_ref
        assert func.__annotations__ == {"return": None}
        assert func.__signature__ == inspect.signature(func_ref)

    def test_ranges(self):
        # Given
        class SimpleModel(BaseModel):
            a: int = Field(ge=0, le=255, description="first arg") 
            b: int = Field(ge=0, le=127, description="second arg") 

        docstring_ref = textwrap.dedent("""\
        Function generated from SimpleModel model.

        Parameters
        ----------
        a : int, optional
            first arg
            Range: 0, 255
        b : int, optional
            second arg
            Range: 0, 127
        """)
        # When
        def dummy(**kw): pass
        func = create_function_from_model(SimpleModel, dummy)

        # Then
        assert func.__doc__ == docstring_ref
