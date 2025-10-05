from enum import IntEnum, verify, UNIQUE
from typing import Self

from pydantic import BaseModel, ConfigDict, Field

from text2synth.patch import JU06APatch


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


# FIXME: this should be merged with JU06APatch class
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
    porta_sw: int = Field(ge=0, le=255, description="Portamento switch")

    # Polyphonic modes
    assign_mode: PolyphonicMode = Field(description="Whether to run in polyphonic mode, solo mode or unison mode")

    @classmethod
    def from_patch(cls, patch: JU06APatch) -> Self:
        """
        Create from JU06AState instance.
        
        Parameters
        ----------
        patch : JU06APatch
            Loaded patch file
            
        Returns
        -------
        JU06AState
            Complete synth state with all parameters set
        """
        return cls(
            osc_range=OscRange(patch.osc_range),
            osc_lfo_mod=patch.osc_lfo_mod,
            pwm=patch.pwm,
            pwm_source=PWMModulation(patch.pwm_source),
            sqr_sw=SquareSwitch(patch.sqr_sw),
            saw_sw=SawSwitch(patch.saw_sw),
            sub_level=patch.sub_level,
            sub_sw=SubSwitch(patch.sub_sw),
            noise_level=patch.noise_level,
            lfo_rate=patch.lfo_rate,
            lfo_delay_time=patch.lfo_delay_time,
            lfo_wave=LFOWave(patch.lfo_wave),
            lfo_trig=LFOTrig(patch.lfo_trig),
            hpf=patch.hpf,
            cutoff=patch.cutoff,
            resonance=patch.resonance,
            env_polarity=EnvPolarity(patch.env_polarity),
            env_mod=patch.env_mod,
            flt_lfo_mod=patch.flt_lfo_mod,
            flt_key_follow=patch.flt_key_follow,
            amp_mode=VCAEnvGate(patch.amp_mode),
            amp_level=patch.amp_level,
            attack=patch.attack,
            decay=patch.decay,
            sustain=patch.sustain,
            release=patch.release,
            delay_time=patch.delay_time,
            delay_feedback=patch.delay_feedback,
            delay_sw=DelaySwitch(patch.delay_sw),
            delay_level=patch.delay_level,
            chorus_sw=ChorusType(patch.chorus_sw),
            porta_time=patch.porta_time,
            porta_sw=patch.porta_sw,
            assign_mode=PolyphonicMode(patch.assign_mode),
        )
