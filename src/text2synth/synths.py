JU_A6_A = {
    # 0 -> 16, 1 -> 8, 2 -> 4
    "dco.range": {"cc": 12, "min": 0, "max": 2},
    "dco.lfo": {"cc": 13, "min": 0, "max": 127},
    "dco.pwm_amount": {"cc": 14, "min": 0, "max": 127},
    "dco.square_switch": {"cc": 16, "min": 0, "max": 1},
    "dco.saw_switch": {"cc": 17, "min": 0, "max": 1},
    "dco.sub": {"cc": 18, "min": 0, "max": 127},
    "dco.sub_switch": {"cc": 28, "min": 0, "max": 1},
    "dco.noise": {"cc": 19, "min": 0, "max": 127},

    "lfo.rate": {"cc": 3, "min": 0, "max": 127},
    "lfo.delay": {"cc": 9, "min": 0, "max": 127},
    # 0 -> triangle, 1 -> square, 2 -> sawtooth 1, 3 -> sawtooth 2, 4 -> sin, 5 -> rand1, 6 -> rand2
    "lfo.wave": {"cc": 29, "min": 0, "max": 6},
    "lfo.trig": {"cc": 30, "min": 0, "max": 1},

    "vcf.cutoff": {"cc": 74, "min": 0, "max": 127},
    "vcf.env": {"cc": 22, "min": 0, "max": 127},
    "vcf.env_polarity": {"cc": 21, "min": 0, "max": 1},
    "vcf.res": {"cc": 71, "min": 0, "max": 127},
    "vcf.lfo": {"cc": 23, "min": 0, "max": 127},
    "vcf.kybd": {"cc": 24, "min": 0, "max": 127},

    # 0 -> MAN, 1 -> LFO, 2 -> ENV
    # NOTE: this is not the same order as the HW switch which is LFO -> MAN -> ENV
    "dco.pwm_modulation": {"cc": 15, "min": 0, "max": 2},

    "hpf.cutoff": {"cc": 20, "min": 0, "max": 127},

    "vca.env_gate": {"cc": 25, "min": 0, "max": 1},
    "vca.level": {"cc": 26, "min": 0, "max": 127},

    "env.attack": {"cc": 73, "min": 0, "max": 127},
    "env.decay": {"cc": 75, "min": 0, "max": 127},
    "env.sustain": {"cc": 27, "min": 0, "max": 127},
    "env.release": {"cc": 72, "min": 0, "max": 127},

    "delay.time": {"cc": 82, "min": 0, "max": 15},
    "delay.feedback": {"cc": 83, "min": 0, "max": 15},
    "delay.switch": {"cc": 89, "min": 0, "max": 1},
    "delay.level": {"cc": 91, "min": 0, "max": 15},

    # 0 -> off, 1 -> I, 2 -> II, 3 -> I+II
    "chorus.type": {"cc": 93, "min": 0, "max": 3},

    # NOTE:: 2 * CC value = encoder value
    "portamento.time": {"cc": 5, "min": 0, "max": 127},
    # NOTE: 0-63 -> off, 64 -> 127 -> on
    "portamento.switch": {"cc": 65, "min": 0, "max": 127},

    # 0,1 -> POLYPHONIC, 2 -> SOLO, 3 -> UNISON
    "polyphonic.mode": {"cc": 86, "min": 0, "max": 3},
    # 5 CC not implemented (not useful)
    # - 1: MODULATION
    # - 11: EXPRESSION PEDAL
    # - 64: HOLD
    # - 87: BEND RANGE
    # - 88: TEMPO SYNC
}
