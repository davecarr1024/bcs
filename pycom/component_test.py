import unittest
import pycom


class ComponentTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Component("a")

    def test_ctor_parent(self) -> None:
        parent = pycom.Component("parent")
        child = pycom.Component("child", parent=parent)
        self.assertIs(child.parent, parent)
        self.assertSetEqual(parent.children, {child})

    def test_ctor_child(self) -> None:
        child = pycom.Component("child")
        parent = pycom.Component("parent", children=frozenset({child}))
        self.assertIs(child.parent, parent)
        self.assertSetEqual(parent.children, {child})

    def test_set_parent(self) -> None:
        child = pycom.Component("child")
        parent = pycom.Component("parent")
        child.parent = parent
        self.assertIs(child.parent, parent)
        self.assertSetEqual(parent.children, {child})

    def test_add_child(self) -> None:
        child = pycom.Component("child")
        parent = pycom.Component("parent")
        parent.add_child(child)
        self.assertIs(child.parent, parent)
        self.assertSetEqual(parent.children, {child})

    def test_remove_child(self) -> None:
        child = pycom.Component("child")
        parent = pycom.Component("parent")
        parent.add_child(child)
        self.assertIs(child.parent, parent)
        self.assertSetEqual(parent.children, {child})
        parent.remove_child(child)
        self.assertIsNone(child.parent)
        self.assertSetEqual(parent.children, frozenset())

    def test_children_by_name(self) -> None:
        child = pycom.Component("child")
        parent = pycom.Component("parent", children=frozenset({child}))
        self.assertDictEqual(parent.children_by_name, {"child": child})

    def test_duplicate_child_name(self) -> None:
        child1 = pycom.Component("child")
        child2 = pycom.Component("child")
        with self.assertRaises(pycom.Component.ValidationError):
            pycom.Component("parent", children=frozenset({child1, child2}))

    def test_get_child(self) -> None:
        child = pycom.Component("child")
        parent = pycom.Component("parent", children=frozenset({child}))
        self.assertIs(parent.child("child"), child)

    def test_get_child_not_found(self) -> None:
        child = pycom.Component("child")
        parent = pycom.Component("parent", children=frozenset({child}))
        with self.assertRaises(pycom.Component.ChildNotFoundError):
            parent.child("invalid_child")

    def test_get_grandchild(self) -> None:
        grandchild = pycom.Component("grandchild")
        child = pycom.Component("child", children=frozenset({grandchild}))
        parent = pycom.Component("parent", children=frozenset({child}))
        self.assertIs(parent.child("child.grandchild"), grandchild)

    def test_get_root(self) -> None:
        grandchild = pycom.Component("grandchild")
        child = pycom.Component("child", children=frozenset({grandchild}))
        parent = pycom.Component("parent", children=frozenset({child}))
        self.assertIs(grandchild.root, parent)
        self.assertIs(child.root, parent)
        self.assertIs(parent.root, parent)

    def test_get_path(self) -> None:
        grandchild = pycom.Component("grandchild")
        child = pycom.Component("child", children=frozenset({grandchild}))
        parent = pycom.Component("parent", children=frozenset({child}))
        self.assertEqual(parent.path, "parent")
        self.assertEqual(child.path, "parent.child")
        self.assertEqual(grandchild.path, "parent.child.grandchild")

    def test_control(self) -> None:
        c = pycom.Control("c")
        a = pycom.Component("a", controls=frozenset({c}))
        self.assertSetEqual(a.controls, frozenset({c}))
        self.assertDictEqual(a.controls_by_name, {"c": c})
        self.assertIs(a.control("c"), c)

    def test_add_control(self) -> None:
        c = pycom.Control("c")
        a = pycom.Component("a")
        a.add_control(c)
        self.assertIs(c.component, a)
        self.assertSetEqual(a.controls, frozenset({c}))

    def test_remove_control(self) -> None:
        c = pycom.Control("c")
        a = pycom.Component("a")
        a.add_control(c)
        self.assertIs(c.component, a)
        self.assertSetEqual(a.controls, frozenset({c}))
        a.remove_control(c)
        self.assertIsNone(c.component)
        self.assertSetEqual(a.controls, frozenset())

    def test_control_not_found(self) -> None:
        with self.assertRaises(pycom.Component.ControlNotFoundError):
            pycom.Component("a").control("c")

    def test_child_control(self) -> None:
        c = pycom.Control("c")
        b = pycom.Component("b", controls=frozenset({c}))
        a = pycom.Component("a", children=frozenset({b}))
        self.assertIs(a.control("b.c"), c)

    def test_all_controls(self) -> None:
        c1 = pycom.Control("c1")
        c2 = pycom.Control("c2")
        c3 = pycom.Control("c3")
        a = pycom.Component("a", controls=frozenset({c1, c2}))
        b = pycom.Component("b", children=frozenset({a}), controls=frozenset({c3}))
        self.assertSetEqual(b.all_controls, frozenset({c1, c2, c3}))

    def test_set_control(self) -> None:
        c = pycom.Control("c")
        a = pycom.Component("a", controls=frozenset({c}))
        b = pycom.Component("b", children=frozenset({a}))
        b.set_control("a.c", True)
        self.assertTrue(c.value)

    def test_set_controls(self) -> None:
        c1 = pycom.Control("c1")
        c2 = pycom.Control("c2")
        a = pycom.Component("a", controls=frozenset({c1, c2}))
        b = pycom.Component("b", children=frozenset({a}))
        b.set_controls("a.c1")
        self.assertTrue(c1.value)
        self.assertFalse(c2.value)
        b.set_controls("a.c2")
        self.assertFalse(c1.value)
        self.assertTrue(c2.value)
