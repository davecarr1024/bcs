import unittest

import bcs


class GroundTest(unittest.TestCase):
    def test_empty(self) -> None:
        bcs.components.power.Ground()

    def test_sets(self) -> None:
        a = bcs.components.Component("c").add_pin("a")
        a.connect(bcs.components.power.Ground().output)
        a.state = True
        a.update_all()
        self.assertFalse(a.state)
