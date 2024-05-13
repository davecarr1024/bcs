import unittest

import bcs


class GroundTest(unittest.TestCase):
    def test_ref(self) -> None:
        bcs.components.ground_

    def test_sets(self) -> None:
        a = bcs.components.Component("c").add_pin("a")
        a.connect(bcs.components.ground_.output)
        a.state = True
        a.update_all()
        self.assertFalse(a.state)
