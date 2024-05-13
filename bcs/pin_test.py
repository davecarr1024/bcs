import unittest

import bcs


class PinTest(unittest.TestCase):
    def test_create(self) -> None:
        c = bcs.Component("c")
        a = bcs.Pin("a", c)
        self.assertIs(a.component, c)
        self.assertDictEqual(dict(c), {"a": a})
        self.assertSetEqual(a.all_connected_objects, {a, c})
        self.assertSetEqual(c.all_connected_objects, {a, c})
        self.assertSetEqual(a.all_connected_pins, {a})

    def test_invalid_duplicate_name(self) -> None:
        c = bcs.Component("c")
        a = bcs.Pin("a", c)
        with self.assertRaises(bcs.Object.Error):
            bcs.Pin("a", c)

    def test_connect(self) -> None:
        c = bcs.Component("c")
        a = bcs.Pin("a", c)
        b = bcs.Pin("b", c)
        a.connect(b)
        self.assertSetEqual(a.connected_pins, {b})
        self.assertSetEqual(b.connected_pins, {a})
        self.assertSetEqual(a.all_connected_pins, {a, b})
        self.assertSetEqual(b.all_connected_pins, {a, b})
        self.assertTrue(a.is_connected(b))
        self.assertTrue(b.is_connected(a))
        self.assertSetEqual(a.all_connected_objects, {a, b, c})
        self.assertSetEqual(b.all_connected_objects, {a, b, c})
        self.assertSetEqual(c.all_connected_objects, {a, b, c})

    def test_disconnect(self) -> None:
        c = bcs.Component("c")
        a = bcs.Pin("a", c)
        b = bcs.Pin("b", c)
        a.connect(b)
        a.disconnect(b)
        self.assertSetEqual(a.connected_pins, set())
        self.assertSetEqual(b.connected_pins, set())
        self.assertSetEqual(a.all_connected_pins, {a})
        self.assertSetEqual(b.all_connected_pins, {b})
        self.assertFalse(a.is_connected(b))
        self.assertFalse(b.is_connected(a))
        self.assertSetEqual(a.all_connected_objects, {a, b, c})
        self.assertSetEqual(b.all_connected_objects, {a, b, c})
        self.assertSetEqual(c.all_connected_objects, {a, b, c})

    def test_set_state(self) -> None:
        c = bcs.Component("c")
        a = bcs.Pin("a", c)
        b = bcs.Pin("b", c)
        a.connect(b)
        self.assertFalse(a.state)
        self.assertFalse(b.state)
        a.state = True
        self.assertTrue(a.state)
        self.assertTrue(b.state)

    def test_propagate_state(self) -> None:
        a = bcs.Pin("a", bcs.Component("c1"))
        b = bcs.Pin("b", bcs.Component("c2"))
        c = bcs.Pin("c", bcs.Component("c3"))
        a.connect(b)
        b.connect(c)
        a.state = True
        self.assertTrue(c.state)
        a.state = False
        self.assertFalse(c.state)
