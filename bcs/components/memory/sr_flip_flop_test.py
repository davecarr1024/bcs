import unittest

import bcs


class SRFlipFlopTest(unittest.TestCase):
    def test_empty(self) -> None:
        bcs.components.memory.SRFlipFLop()

    def test_set(self) -> None:
        ff = bcs.components.memory.SRFlipFLop()
        clk = bcs.components.clock.Clock()
        clk.output.connect(ff.clk)
        ff.states = dict(s=True, r=False)
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                s=True,
                r=False,
                clk=False,
                q=True,
                q_inverse=False,
            ),
            repr(ff),
        )

    def test_reset(self) -> None:
        ff = bcs.components.memory.SRFlipFLop()
        clk = bcs.components.clock.Clock()
        clk.output.connect(ff.clk)
        ff.states = dict(s=False, r=True)
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                s=False,
                r=True,
                clk=False,
                q=False,
                q_inverse=True,
            ),
            repr(ff),
        )

    def test_set_ignores_input(self) -> None:
        ff = bcs.components.memory.SRFlipFLop()
        clk = bcs.components.clock.Clock()
        clk.output.connect(ff.clk)
        ff.states = dict(s=True, r=False)
        clk.pulse()
        ff.states = dict(s=False, r=True)
        self.assertDictEqual(
            ff.states,
            dict(
                s=False,
                r=True,
                clk=False,
                q=True,
                q_inverse=False,
            ),
            repr(ff),
        )

    def test_reset_ignores_input(self) -> None:
        ff = bcs.components.memory.SRFlipFLop()
        clk = bcs.components.clock.Clock()
        clk.output.connect(ff.clk)
        ff.states = dict(s=False, r=True)
        clk.pulse()
        ff.states = dict(s=True, r=False)
        self.assertDictEqual(
            ff.states,
            dict(
                s=True,
                r=False,
                clk=False,
                q=False,
                q_inverse=True,
            ),
            repr(ff),
        )

    def test_set_and_reset(self) -> None:
        ff = bcs.components.memory.SRFlipFLop()
        clk = bcs.components.clock.Clock()
        clk.output.connect(ff.clk)
        ff.states = dict(s=True, r=False)
        clk.pulse()
        ff.states = dict(s=False, r=True)
        self.assertDictEqual(
            ff.states,
            dict(
                s=False,
                r=True,
                clk=False,
                q=True,
                q_inverse=False,
            ),
            repr(ff),
        )
        clk.pulse()
        self.assertDictEqual(
            ff.states,
            dict(
                s=False,
                r=True,
                clk=False,
                q=False,
                q_inverse=True,
            ),
            repr(ff),
        )
