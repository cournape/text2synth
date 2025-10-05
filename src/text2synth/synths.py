JU_A6_A = {
    # 0 -> 16, 1 -> 8, 2 -> 4
    "dco.range": {"cc": 12, "min": 0, "max": 2, "patch_attribute": "osc_range"},
    "dco.lfo": {"cc": 13, "min": 0, "max": 127, "patch_attribute": "osc_lfo_mod"},
    "dco.pwm_amount": {"cc": 14, "min": 0, "max": 127, "patch_attribute": "pwm"},
    "dco.square_switch": {"cc": 16, "min": 0, "max": 1, "patch_attribute": "sqr_sw"},
    "dco.saw_switch": {"cc": 17, "min": 0, "max": 1, "patch_attribute": "saw_sw"},
    "dco.sub": {"cc": 18, "min": 0, "max": 127, "patch_attribute": "sub_level"},
    "dco.sub_switch": {"cc": 28, "min": 0, "max": 1, "patch_attribute": "sub_sw"},
    "dco.noise": {"cc": 19, "min": 0, "max": 127, "patch_attribute": "noise_level"},

    "lfo.rate": {"cc": 3, "min": 0, "max": 127, "patch_attribute": "lfo_rate"},
    "lfo.delay": {"cc": 9, "min": 0, "max": 127, "patch_attribute": "lfo_delay_time"},
    # 0 -> triangle, 1 -> square, 2 -> sawtooth 1, 3 -> sawtooth 2, 4 -> sin, 5 -> rand1, 6 -> rand2
    "lfo.wave": {"cc": 29, "min": 0, "max": 6, "patch_attribute": "lfo_wave"},
    "lfo.trig": {"cc": 30, "min": 0, "max": 1, "patch_attribute": "lfo_trig"},

    "vcf.cutoff": {"cc": 74, "min": 0, "max": 127, "patch_attribute": "cutoff"},
    "vcf.env": {"cc": 22, "min": 0, "max": 127, "patch_attribute": "env_mod"},
    "vcf.env_polarity": {"cc": 21, "min": 0, "max": 1, "patch_attribute": "env_polarity"},
    "vcf.res": {"cc": 71, "min": 0, "max": 127, "patch_attribute": "resonance"},
    "vcf.lfo": {"cc": 23, "min": 0, "max": 127, "patch_attribute": "flt_lfo_mod"},
    "vcf.kybd": {"cc": 24, "min": 0, "max": 127, "patch_attribute": "flt_key_follow"},

    # 0 -> MAN, 1 -> LFO, 2 -> ENV
    # NOTE: this is not the same order as the HW switch which is LFO -> MAN -> ENV
    "dco.pwm_modulation": {"cc": 15, "min": 0, "max": 2, "patch_attribute": "pwm_source"},

    "hpf.cutoff": {"cc": 20, "min": 0, "max": 127, "patch_attribute": "hpf"},

    "vca.env_gate": {"cc": 25, "min": 0, "max": 1, "patch_attribute": "amp_mode"},
    "vca.level": {"cc": 26, "min": 0, "max": 127, "patch_attribute": "amp_level"},

    "env.attack": {"cc": 73, "min": 0, "max": 127, "patch_attribute": "attack"},
    "env.decay": {"cc": 75, "min": 0, "max": 127, "patch_attribute": "decay"},
    "env.sustain": {"cc": 27, "min": 0, "max": 127, "patch_attribute": "sustain"},
    "env.release": {"cc": 72, "min": 0, "max": 127, "patch_attribute": "release"},

    "delay.time": {"cc": 82, "min": 0, "max": 15, "patch_attribute": "delay_time"},
    "delay.feedback": {"cc": 83, "min": 0, "max": 15, "patch_attribute": "delay_feedback"},
    "delay.switch": {"cc": 89, "min": 0, "max": 1, "patch_attribute": "delay_sw"},
    "delay.level": {"cc": 91, "min": 0, "max": 15, "patch_attribute": "delay_level"},

    # 0 -> off, 1 -> I, 2 -> II, 3 -> I+II
    "chorus.type": {"cc": 93, "min": 0, "max": 3, "patch_attribute": "chorus_sw"},

    # NOTE:: 2 * CC value = encoder value
    "portamento.time": {"cc": 5, "min": 0, "max": 127, "patch_attribute": "porta_time"},
    # NOTE: 0-63 -> off, 64 -> 127 -> on
    "portamento.switch": {"cc": 65, "min": 0, "max": 127, "patch_attribute": "porta_sw"},

    # 0,1 -> POLYPHONIC, 2 -> SOLO, 3 -> UNISON
    "polyphonic.mode": {"cc": 86, "min": 0, "max": 3, "patch_attribute": "assign_mode"},
    # 5 CC not implemented (not useful)
    # - 1: MODULATION
    # - 11: EXPRESSION PEDAL
    # - 64: HOLD
    # - 87: BEND RANGE
    # - 88: TEMPO SYNC
}
}
