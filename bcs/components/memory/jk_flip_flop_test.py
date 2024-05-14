import unittest

import bcs


class JKFlipFlopTest(unittest.TestCase):
    def test_set(self) -> None:
        ff = bcs.components.memory.JKFlipFlop()
        ff.j.state = True
        ff.k.state = False
        ff.clk.state = True
        ff.clk.state = False
        self.assertDictEqual(
            ff.states,
            {
                "j": True,
                "k": False,
                "clk": False,
                "q": True,
                "q_inverse": False,
            },
        )
