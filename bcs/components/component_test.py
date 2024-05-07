import unittest

from . import component


class ComponentTest(unittest.TestCase):
    def test_run_empty(self) -> None:
        component.Component().run_until_stable()

    def test_pass_through(self) -> None:
        c = component.Component()
        a = c.add_connector("a")
        b = c.add_connector("b")
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        a.run_until_stable()
        self.assertTrue(b.state)
