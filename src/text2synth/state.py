import re

from enum import IntEnum, verify, UNIQUE
from typing import Self

import mido

from pydantic import BaseModel, ConfigDict, Field

from .synths import JU_A6_A


# List of fields that support a range of 0..255 at the synth level. This list
# was created automatically from the CLI by analyzing a bynch of real patches
DOUBLE_ATTRIBUTES = {
    "amp_level",
    "attack",
    "cutoff",
    "decay",
    "env_mod",
    "flt_key_follow",
    "flt_lfo_mod",
    "hpf",
    "lfo_delay_time",
    "lfo_rate",
    "noise_level",
    "osc_lfo_mod",
    "pwm",
    "release",
    "resonance",
    "sub_level",
    "sustain",
}


@verify(UNIQUE)
class OscRange(IntEnum):
    """DCO Range: octave selection."""
    SIXTEEN = 0  # 16'
    EIGHT = 1    # 8'
    FOUR = 2     # 4'


@verify(UNIQUE)
class LFOWave(IntEnum):
    """LFO waveform selection."""
    TRIANGLE = 0
    SQUARE = 1
    SAWTOOTH_1 = 2
    SAWTOOTH_2 = 3
    SIN = 4
    RAND_1 = 5
    RAND_2 = 6


@verify(UNIQUE)
class LFOTrig(IntEnum):
    """LFO trigger mode."""
    OFF = 0
    ON = 1


@verify(UNIQUE)
class SquareSwitch(IntEnum):
    """Square wave on/off."""
    OFF = 0
    ON = 1


@verify(UNIQUE)
class SawSwitch(IntEnum):
    """Saw wave on/off."""
    OFF = 0
    ON = 1


@verify(UNIQUE)
class SubSwitch(IntEnum):
    """Sub oscillator on/off."""
    OFF = 0
    ON = 1


@verify(UNIQUE)
class PWMModulation(IntEnum):
    """PWM modulation source."""
    MAN = 0  # Manual
    LFO = 1
    ENV = 2


@verify(UNIQUE)
class EnvPolarity(IntEnum):
    """Filter envelope polarity."""
    NEGATIVE = 0
    POSITIVE = 1


@verify(UNIQUE)
class VCAEnvGate(IntEnum):
    """VCA envelope/gate mode."""
    GATE = 0
    ENV = 1


@verify(UNIQUE)
class DelaySwitch(IntEnum):
    """Delay on/off."""
    OFF = 0
    ON = 1


@verify(UNIQUE)
class ChorusType(IntEnum):
    """Chorus type selection."""
    OFF = 0
    I = 1
    II = 2
    I_AND_II = 3


@verify(UNIQUE)
class PortamentoSwitch(IntEnum):
    OFF = 0
    ON = 1


@verify(UNIQUE)
class PolyphonicMode(IntEnum):
    """Polyphonic mode selection."""
    POLYPHONIC = 0
    SOLO = 2
    UNISON = 3


class JU06AState(BaseModel):
    """Complete JU-06A synthesizer state with all parameters.

    Values are represented in "UI model", i.e. as represented from the HW
    """
    model_config = ConfigDict(validate_assignment=True)

    # DCO (Digital Controlled Oscillator)
    osc_range: OscRange = Field(description="DCO range/octave selection")
    osc_lfo_mod: int = Field(ge=0, le=255, description="DCO LFO modulation amount")
    pwm: int = Field(ge=0, le=255, description="Pulse width modulation amount")
    pwm_source: PWMModulation = Field(description="PWM modulation source")
    sqr_sw: SquareSwitch = Field(description="Square wave switch")
    saw_sw: SawSwitch = Field(description="Saw wave switch")
    sub_level: int = Field(ge=0, le=255, description="Sub oscillator level")
    sub_sw: SubSwitch = Field(description="Sub oscillator switch")
    noise_level: int = Field(ge=0, le=255, description="Noise level")
    
    # LFO (Low Frequency Oscillator)
    lfo_rate: int = Field(ge=0, le=255, description="LFO rate/speed")
    lfo_delay_time: int = Field(ge=0, le=255, description="LFO delay time")
    lfo_wave: LFOWave = Field(description="LFO waveform")
    lfo_trig: LFOTrig = Field(description="LFO trigger mode")
    
    # VCF (Voltage Controlled Filter)
    hpf: int = Field(ge=0, le=255, description="High-pass filter cutoff")
    cutoff: int = Field(ge=0, le=255, description="Low-pass filter cutoff")
    resonance: int = Field(ge=0, le=255, description="Filter resonance")
    env_polarity: EnvPolarity = Field(description="Filter envelope polarity")
    env_mod: int = Field(ge=0, le=255, description="Filter envelope modulation")
    flt_lfo_mod: int = Field(ge=0, le=255, description="Filter LFO modulation")
    flt_key_follow: int = Field(ge=0, le=255, description="Filter keyboard follow")
    
    # VCA (Voltage Controlled Amplifier)
    amp_mode: VCAEnvGate = Field(description="VCA envelope/gate mode")
    amp_level: int = Field(ge=0, le=255, description="VCA level")
    
    # Envelope
    attack: int = Field(ge=0, le=255, description="Envelope attack time")
    decay: int = Field(ge=0, le=255, description="Envelope decay time")
    sustain: int = Field(ge=0, le=255, description="Envelope sustain level")
    release: int = Field(ge=0, le=255, description="Envelope release time")
    
    # Delay
    delay_time: int = Field(ge=0, le=15, description="Delay time")
    delay_feedback: int = Field(ge=0, le=15, description="Delay feedback")
    delay_sw: DelaySwitch = Field(description="Delay switch")
    delay_level: int = Field(ge=0, le=15, description="Delay level")
    
    # Chorus
    chorus_sw: ChorusType = Field(description="Chorus type")
    
    # Portamento
    porta_time: int = Field(ge=0, le=255, description="Portamento time")
    porta_sw: PortamentoSwitch = Field(description="Portamento switch")

    # Polyphonic modes
    assign_mode: PolyphonicMode = Field(description="Whether to run in polyphonic mode, solo mode or unison mode")

    @classmethod
    def from_path(cls, path: str) -> Self:
        """
        Create from a patch file stored as PRM file.
        
        Parameters
        ----------
        patch : str
            Loaded patch file
            
        Returns
        -------
        JU06AState
            Complete synth state with all parameters set
        """
        parsed_values = {}

        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        for i, line in enumerate(lines):
            # Match pattern: "PARAMETER (value);" or "PARAMETER(value);"
            match = re.match(r'^(.+?)\s*\((.+?)\)\s*;?$', line)
            if not match:
                continue

            attr_name_raw = match.group(1).strip()
            value_raw = match.group(2).strip()

            # Convert attribute name to Python convention
            attr_name = attr_name_raw.lower().replace(' ', '_')

            # Determine if this is the last row (PATCH_NAME)
            is_last_row = (i == len(lines) - 1)

            # Parse value: string for last row, integer for others
            if is_last_row:
                value = value_raw
            else:
                value = int(value_raw)

            parsed_values[attr_name] = value

        return cls(
            osc_range=OscRange(parsed_values["osc_range"]),
            osc_lfo_mod=parsed_values["osc_lfo_mod"],
            pwm=parsed_values["pwm"],
            pwm_source=PWMModulation(parsed_values["pwm_source"]),
            sqr_sw=SquareSwitch(parsed_values["sqr_sw"]),
            saw_sw=SawSwitch(parsed_values["saw_sw"]),
            sub_level=parsed_values["sub_level"],
            sub_sw=SubSwitch(parsed_values["sub_sw"]),
            noise_level=parsed_values["noise_level"],
            lfo_rate=parsed_values["lfo_rate"],
            lfo_delay_time=parsed_values["lfo_delay_time"],
            lfo_wave=LFOWave(parsed_values["lfo_wave"]),
            lfo_trig=LFOTrig(parsed_values["lfo_trig"]),
            hpf=parsed_values["hpf"],
            cutoff=parsed_values["cutoff"],
            resonance=parsed_values["resonance"],
            env_polarity=EnvPolarity(parsed_values["env_polarity"]),
            env_mod=parsed_values["env_mod"],
            flt_lfo_mod=parsed_values["flt_lfo_mod"],
            flt_key_follow=parsed_values["flt_key_follow"],
            amp_mode=VCAEnvGate(parsed_values["amp_mode"]),
            amp_level=parsed_values["amp_level"],
            attack=parsed_values["attack"],
            decay=parsed_values["decay"],
            sustain=parsed_values["sustain"],
            release=parsed_values["release"],
            delay_time=parsed_values["delay_time"],
            delay_feedback=parsed_values["delay_feedback"],
            delay_sw=DelaySwitch(parsed_values["delay_sw"]),
            delay_level=parsed_values["delay_level"],
            chorus_sw=ChorusType(parsed_values["chorus_sw"]),
            porta_time=parsed_values["porta_time"],
            porta_sw=parsed_values["porta_sw"],
            assign_mode=PolyphonicMode(parsed_values["assign_mode"]),
        )

    def to_path(self, path, patch_name="NEW PATCH"):
        """
        Save the state content to the given path.

        Parameters
        ----------
        filepath : str
            Output file path (should end in .PRN)
        patch_name : str
            Name for the patch.
        """
        # PRM files are in CRLF format
        with open(path, 'w', encoding='ascii', newline='') as f:
            self.to_file(f, patch_name)

    def to_file(self, fp, patch_name="NEW PATCH"):
        """
        Save the state content to the given file.

        Parameters
        ----------
        fp : file-like object
            file object to write into
        patch_name : str
            Name for the patch.
        """

        lines = [
            f"LFO RATE        ({self.lfo_rate});",
            f"LFO DELAY TIME  ({self.lfo_delay_time});",
            f"LFO WAVE        ({self.lfo_wave.value});",
            f"LFO TRIG        ({self.lfo_trig.value});",
            f"OSC RANGE       ({self.osc_range.value});",
            f"OSC LFO MOD     ({self.osc_lfo_mod});",
            f"PWM             ({self.pwm});",
            f"PWM SOURCE      ({self.pwm_source.value});",
            f"SQR SW          ({self.sqr_sw.value});",
            f"SAW SW          ({self.saw_sw.value});",
            f"SUB LEVEL       ({self.sub_level});",
            f"NOISE LEVEL     ({self.noise_level});",
            f"SUB SW          ({self.sub_sw.value});",
            f"HPF             ({self.hpf});",
            f"CUTOFF          ({self.cutoff});",
            f"RESONANCE       ({self.resonance});",
            f"ENV POLARITY    ({self.env_polarity.value});",
            f"ENV MOD         ({self.env_mod});",
            f"FLT LFO MOD     ({self.flt_lfo_mod});",
            f"FLT KEY FOLLOW  ({self.flt_key_follow});",
            f"AMP MODE        ({self.amp_mode.value});",
            f"AMP LEVEL       ({self.amp_level});",
            f"ATTACK          ({self.attack});",
            f"DECAY           ({self.decay});",
            f"SUSTAIN         ({self.sustain});",
            f"RELEASE         ({self.release});",
            f"CHORUS SW       ({self.chorus_sw.value});",
            f"DELAY LEVEL     ({self.delay_level});",
            f"DELAY TIME      ({self.delay_time});",
            f"DELAY FEEDBACK  ({self.delay_feedback});",
            f"DELAY SW        ({self.delay_sw.value});",
            f"PORTA SW        ({self.porta_sw});",
            f"PORTA TIME      ({self.porta_time});",
            f"ASSIGN MODE     ({self.assign_mode.value});",
            "BEND RANGE      (12);",  # Not in self, use default
            "TEMPO SYNC      (0);",   # Not in self, use default
            f"PATCH_NAME({patch_name});",
            "",
        ]

        fp.write('\r\n'.join(lines))

    def attribute_to_patch_key(self, attribute):
        """ Convert the given attribute name into the key used in .PRN files.
        """
        return attribute.replace("_", " ").upper()

    def to_cc_messages(self):
        """ Create a list of midi messages that when applied to the synth, will
        update the synth to the current state.
        """
        messages = []
        for data in JU_A6_A.values():
            cc = data["cc"]

            patch_attribute = data["patch_attribute"]
            value = getattr(self, patch_attribute)
            if patch_attribute in DOUBLE_ATTRIBUTES:
                cc_value = value // 2
            elif isinstance(value, IntEnum):
                if isinstance(value, PortamentoSwitch):
                    # cc value [0, 63[ -> off, [63-128[ -> on
                    cc_value = 63 * value
                else:
                    cc_value = value
            else:
                cc_value = value

            messages.append(mido.Message("control_change", control=cc, value=cc_value))

        return messages
