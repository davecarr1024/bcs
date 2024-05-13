import unittest

import bcs


class JKFlipFlopTest(unittest.TestCase):
    def test_set(self) -> None:
        ff = bcs.components.memory.JKFlipFlop()
        ff.print_all_states("\nstart:\n")
        ff.j.state = True
        ff.print_all_states("\n/set j:\n")
        ff.k.state = False
        ff.print_all_states("\n/set k:\n")
        ff.clk.state = True
        ff.print_all_states("\n/set clk:\n")
        ff.clk.state = False
        ff.print_all_states("\n/unset clk:\n")
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
