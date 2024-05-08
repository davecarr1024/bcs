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
            a.validate_all_if_enabled()
            c.validate_all_if_enabled()

    def test_run_empty(self) -> None:
        component.Component().run_until_stable()

    def test_add_connector(self) -> None:
        c = component.Component("c")
        a = c.add_connector("a")
        self.assertIs(a.component, c)
        self.assertCountEqual([a], c.connectors)
        self.assertIs(c["a"], a)
        self.assertCountEqual(a.all_connected_objects, [a, c])
        self.assertCountEqual(c.all_connected_objects, [a, c])

    def test_add_two_connectors(self) -> None:
        c = component.Component("c")
        a = c.add_connector("a")
        b = c.add_connector("b")
        self.assertIs(a.component, c)
        self.assertIs(b.component, c)
        self.assertCountEqual(c.connectors, [a, b])
        self.assertIs(c["a"], a)
        self.assertIs(c["b"], b)
        self.assertCountEqual(a.all_connected_objects, [a, b, c])
        self.assertCountEqual(b.all_connected_objects, [a, b, c])
        self.assertCountEqual(c.all_connected_objects, [a, b, c])

    def test_pass_through(self) -> None:
        c = component.Component("c")
        a = c.add_connector("a")
        b = c.add_connector("b")
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        self.assertEqual(
            len(a.all_connected_objects),
            len(c.all_connected_objects),
            msg=f"{a.all_connected_objects} {c.all_connected_objects}",
        )
        c.run_until_stable_with_states(a=True, b=True)

    def test_pass_through_fail(self) -> None:
        c = component.Component("c")
        a = c.add_connector("a")
        b = c.add_connector("b")
        a.connect(b)
        self.assertFalse(b.state)
        a.state = True
        with self.assertRaises(Exception):
            c.run_until_stable_with_states(a=True, b=False)

    def test_subcomponent(self) -> None:
        c = component.Component()
        a = c.add_connector("a")
        b = c.add_connector("b")
        b.connect(~a)
        a.state = True
        b.state = True
        c.run_until_stable_with_states(a=True, b=False)
