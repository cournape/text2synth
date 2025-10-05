import pathlib


from text2synth.patch import JU06APatch
from text2synth.state import JU06AState


PAD_PRM = pathlib.Path(__file__).parent / "pad.prm"


class TestJU06AState:
    def test_roundtrip(self, tmpdir):
        # Given
        path = PAD_PRM
        out = tmpdir / "out.pad"

        with open(path) as fp:
            r_content = fp.read()

        # When
        patch = JU06APatch.from_path(str(path))
        state = JU06AState.from_patch(patch)

        state.to_path(out, "SIMPLE PAD")

        with open(out) as fp:
            content = fp.read()

        # Then
        assert r_content == content
