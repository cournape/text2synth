import inspect
import io
import textwrap

from typing import Optional
from unittest import mock

from fastmcp import Client
from mcp.types import Tool, CallToolRequest, CallToolResult, TextContent
from pydantic import BaseModel, Field

from text2synth.mcp_server import INIT_106, create_function_from_model
from text2synth.state import JU06AState


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
        assert func.__annotations__ == func_ref.__annotations__
        assert func.__signature__ == inspect.signature(func_ref)

    def test_simple(self):
        # Given
        class SimpleModel(BaseModel):
            a: int = Field(description="first arg")
            b: int = Field(description="second arg")

        def func_ref(a: Optional[int] = None, b: Optional[int] = None) -> None:
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
        assert func.__annotations__ == func_ref.__annotations__
        assert func.__signature__ == inspect.signature(func_ref)

    def test_ranges(self):
        # Given
        class SimpleModel(BaseModel):
            a: int = Field(ge=0, le=255, description="first arg")
            b: int = Field(ge=0, le=127, description="second arg")

        def func_ref(a: Optional[int] = None, b: Optional[int] = None) -> None:
            pass

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
        assert func.__annotations__ == func_ref.__annotations__


class TestText2SynthMCPIntegration:
    @mock.patch('text2synth.mcp_server.apply_state_to_synth')
    async def test_reset(self, apply_state_to_synth):
        # Given
        from text2synth.mcp_server import server

        # When
        async with Client(server) as client:
            result = await client.call_tool("reset", {})

        # Then
        assert apply_state_to_synth.called
        assert not result.is_error

    @mock.patch('text2synth.mcp_server.apply_state_to_synth')
    async def test_update_synth_state(self, apply_state_to_synth):
        # Given
        from text2synth.mcp_server import server

        r_state = JU06AState.from_file(io.StringIO(INIT_106))
        r_state.cutoff = 42

        # When
        async with Client(server) as client:
            result = await client.call_tool("update_synth_state", {"cutoff": r_state.cutoff})

        # Then
        apply_state_to_synth.assert_called_with(r_state)
