import unittest
import bcs


class BcsTest(unittest.TestCase):
    def test_empty_component(self) -> None:
        component = bcs.components.Component()
        component.run_until_stable()

    def test_connection(self) -> None:
        c = bcs.components.Component()
        a = c.add_connector("a")
        b = c.add_connector("b")
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        a.run_until_stable()
        self.assertTrue(b.state)
