import unittest

import bcs


class PowerTest(unittest.TestCase):
    def test_ref(self) -> None:
        bcs.components.power_

    def test_sets(self) -> None:
        a = bcs.components.Component("c").add_pin("a")
        a.connect(bcs.components.power_.output)
        a.state = False
        a.update_all()
        self.assertTrue(a.state)
