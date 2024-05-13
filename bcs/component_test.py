import unittest

import bcs


class ComponentTest(unittest.TestCase):
    def test_empty(self) -> None:
        bcs.Component()

    def test_no_name(self) -> None:
        self.assertEqual(bcs.Component().name, "Component")

    def test_name(self) -> None:
        self.assertEqual(bcs.Component("c").name, "c")

    def test_add_pin(self) -> None:
        c = bcs.Component("c")
        a = c.add_pin("a")
        self.assertIs(a.component, c)
        self.assertDictEqual(dict(c), {"a": a})
        self.assertSetEqual(a.all_connected_objects, {a, c})
        self.assertSetEqual(c.all_connected_objects, {a, c})
