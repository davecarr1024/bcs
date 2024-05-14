import unittest

import bcs


class DFlipFlopTest(unittest.TestCase):
    def test_set(self) -> None:
        ff = bcs.components.memory.DFlipFlop()
        clk = bcs.components.clock.Clock()
        ff.clk.connect(clk.output)
        ff.states = dict(
            d=True,
            enable=True,
        )
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                d=True,
                enable=True,
                clk=False,
                q=True,
                q_inverse=False,
            ),
            repr(ff),
        )

    def test_reset(self) -> None:
        ff = bcs.components.memory.DFlipFlop()
        clk = bcs.components.clock.Clock()
        ff.clk.connect(clk.output)
        ff.states = dict(
            d=False,
            enable=True,
        )
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                d=False,
                enable=True,
                clk=False,
                q=False,
                q_inverse=True,
            ),
            repr(ff),
        )

    def test_no_set_when_disabled(self) -> None:
        ff = bcs.components.memory.DFlipFlop()
        clk = bcs.components.clock.Clock()
        ff.clk.connect(clk.output)
        ff.states = dict(
            d=True,
            enable=True,
        )
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                d=True,
                enable=True,
                clk=False,
                q=True,
                q_inverse=False,
            ),
            repr(ff),
        )
        ff.states = dict(
            d=False,
            enable=False,
        )
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                d=False,
                enable=False,
                clk=False,
                q=True,
                q_inverse=False,
            ),
            repr(ff),
        )

    def test_no_reset_when_disabled(self) -> None:
        ff = bcs.components.memory.DFlipFlop()
        clk = bcs.components.clock.Clock()
        ff.clk.connect(clk.output)
        ff.states = dict(
            d=False,
            enable=True,
        )
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                d=False,
                enable=True,
                clk=False,
                q=False,
                q_inverse=True,
            ),
            repr(ff),
        )
        ff.states = dict(
            d=True,
            enable=False,
        )
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                d=True,
                enable=False,
                clk=False,
                q=False,
                q_inverse=True,
            ),
            repr(ff),
        )
