import pathlib

import pytest

from text2synth.patch import JU06APatch
from text2synth.state import JU06AState


PAD_PRM = pathlib.Path(__file__).parent / "pad.prm"


def state_to_prn_file(state: JU06AState, filepath, patch_name="New Patch"):
    """
    Save a JU06AState instance as a .PRN patch file.

    Parameters
    ----------
    state : JU06AState
        Synthesizer state to save
    filepath : str
        Output file path (should end in .PRN)
    patch_name : str
        Name for the patch (max ~16 characters recommended)
    """
    lines = [
        f"LFO RATE        ({state.lfo_rate});",
        f"LFO DELAY TIME  ({state.lfo_delay_time});",
        f"LFO WAVE        ({state.lfo_wave.value});",
        f"LFO TRIG        ({state.lfo_trig.value});",
        f"OSC RANGE       ({state.osc_range.value});",
        f"OSC LFO MOD     ({state.osc_lfo_mod});",
        f"PWM             ({state.pwm});",
        f"PWM SOURCE      ({state.pwm_source.value});",
        f"SQR SW          ({state.sqr_sw.value});",
        f"SAW SW          ({state.saw_sw.value});",
        f"SUB LEVEL       ({state.sub_level});",
        f"NOISE LEVEL     ({state.noise_level});",
        f"SUB SW          ({state.sub_sw.value});",
        f"HPF             ({state.hpf});",
        f"CUTOFF          ({state.cutoff});",
        f"RESONANCE       ({state.resonance});",
        f"ENV POLARITY    ({state.env_polarity.value});",
        f"ENV MOD         ({state.env_mod});",
        f"FLT LFO MOD     ({state.flt_lfo_mod});",
        f"FLT KEY FOLLOW  ({state.flt_key_follow});",
        f"AMP MODE        ({state.amp_mode.value});",
        f"AMP LEVEL       ({state.amp_level});",
        f"ATTACK          ({state.attack});",
        f"DECAY           ({state.decay});",
        f"SUSTAIN         ({state.sustain});",
        f"RELEASE         ({state.release});",
        f"CHORUS SW       ({state.chorus_sw.value});",
        f"DELAY LEVEL     ({state.delay_level});",
        f"DELAY TIME      ({state.delay_time});",
        f"DELAY FEEDBACK  ({state.delay_feedback});",
        f"DELAY SW        ({state.delay_sw.value});",
        f"PORTA SW        ({state.porta_sw});",
        f"PORTA TIME      ({state.porta_time});",
        f"ASSIGN MODE     ({state.assign_mode.value});",
        f"BEND RANGE      (12);",  # Not in state, use default
        f"TEMPO SYNC      (0);",   # Not in state, use default
        f"PATCH_NAME({patch_name});",
        "",
    ]
    
    with open(filepath, 'w', encoding='ascii', newline='') as f:
        f.write('\r\n'.join(lines))


class TestJU06AState:
    def test_roundtrip(self, tmpdir):
        # Given
        path = PAD_PRM
        out = tmpdir / "out.pad"

        with open(path) as fp:
            r_content = fp.read()

        # When
        patch = JU06APatch.from_path(path)
        state = JU06AState.from_patch(patch)

        state_to_prn_file(state, out, "SIMPLE PAD")

        with open(out) as fp:
            content = fp.read()

        # Then
        assert r_content == content
