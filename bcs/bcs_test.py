import unittest
import bcs


class BcsTest(unittest.TestCase):
    def test_connection(self) -> None:
        c = bcs.components.Component()
        a = c.add_connector("a")
        b = c.add_connector("b")
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        a.run_until_stable()
        self.assertTrue(b.state)
