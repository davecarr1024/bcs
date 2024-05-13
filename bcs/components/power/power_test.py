import unittest

import bcs


class PowerTest(unittest.TestCase):
    def test_empty(self) -> None:
        bcs.components.power.Power()

    def test_sets(self) -> None:
        a = bcs.components.Component("c").add_pin("a")
        a.connect(bcs.components.power.Power().output)
        a.state = False
        a.update_all()
        self.assertTrue(a.state)
