import unittest

import bcs
from bcs.components import logic

from . import component


class ComponentTest(unittest.TestCase):
    def test_duplicate_connector(self) -> None:
        with self.assertRaises(component.Component.ValidationError):
            c = component.Component()
            a = bcs.Connector(name="a", component=c)
            b = bcs.Connector(name="a", component=c)

    def test_connector_disconnected(self) -> None:
        with self.assertRaises(component.Component.ValidationError):
            c = component.Component()
            a = bcs.Connector(name="a", component=c)
            a.component = component.Component()
            a.validate_all()
            c.validate_all()

    def test_run_empty(self) -> None:
        component.Component().run_until_stable()

    def test_pass_through(self) -> None:
        c = component.Component()
        a = c.add_connector("a")
        b = c.add_connector("b")
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        c.run_until_stable_with_state(a=True, b=True)

    def test_pass_through_fail(self) -> None:
        c = component.Component()
        a = c.add_connector("a")
        b = c.add_connector("b")
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        with self.assertRaises(Exception):
            c.run_until_stable_with_state(a=True, b=False)

    def test_subcomponent(self) -> None:
        c = component.Component()
        a = c.add_connector("a")
        b = c.add_connector("b")
        not_ = logic.Not()
        c["a"].connect(not_["a"])
        not_["o"].connect(c["b"])
        c["a"].state = True
        c["b"].run_until_stable_with_state(False)
        c["a"].state = False
        c["b"].run_until_stable_with_state(True)
