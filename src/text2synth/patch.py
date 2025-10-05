import re

from dataclasses import dataclass
from typing import Self


@dataclass
class JU06APatch:
    """JU-06A Synthesizer patch data model."""
    lfo_rate: int
    lfo_delay_time: int
    lfo_wave: int
    lfo_trig: int
    osc_range: int
    osc_lfo_mod: int
    pwm: int
    pwm_source: int
    sqr_sw: int
    saw_sw: int
    sub_level: int
    noise_level: int
    sub_sw: int
    hpf: int
    cutoff: int
    resonance: int
    env_polarity: int
    env_mod: int
    flt_lfo_mod: int
    flt_key_follow: int
    amp_mode: int
    amp_level: int
    attack: int
    decay: int
    sustain: int
    release: int
    chorus_sw: int
    delay_level: int
    delay_time: int
    delay_feedback: int
    delay_sw: int
    porta_sw: int
    porta_time: int
    assign_mode: int
    bend_range: int
    tempo_sync: int
    patch_name: str

    @classmethod
    def from_path(cls, filepath: str) -> Self:
        """
        Load a JU-06A patch from a .prn file and parse it into an object.

        Parameters
        ----------
        filepath : str
            Path to the patch file

        Returns
        -------
        JU06APatch
            Parsed JU-06A synthesizer patch with all parameter values
        """
        parsed_values = {}

        with open(filepath, 'r', encoding='utf-8') as f:
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

        return cls(**parsed_values)

    def attribute_to_patch_key(self, attribute):
        """ Convert the given attribute name into the key used in .PRN files.
        """
        return attribute.replace("_", " ").upper()
