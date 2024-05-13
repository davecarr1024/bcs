import unittest

import bcs


class ComponentTest(unittest.TestCase):
    def test_empty(self) -> None:
        bcs.components.Component()

    def test_no_name(self) -> None:
        self.assertEqual(bcs.components.Component().name, "Component")

    def test_name(self) -> None:
        self.assertEqual(bcs.components.Component("c").name, "c")

    def test_add_pin(self) -> None:
        c = bcs.components.Component("c")
        a = c.add_pin("a")
        self.assertIs(a.component, c)
        self.assertDictEqual(dict(c), {"a": a})
        self.assertSetEqual(a.all_connected_objects, {a, c})
        self.assertSetEqual(c.all_connected_objects, {a, c})

    def test_add_child(self) -> None:
        parent = bcs.components.Component("parent")
        child = bcs.components.Component("child", parent)
        self.assertIs(child.parent, parent)
        self.assertIn(child, parent.children)
        self.assertSetEqual(child.all_connected_objects, {child, parent})
        self.assertSetEqual(parent.all_connected_objects, {child, parent})
