import unittest

import pycom


class SignalTest(unittest.TestCase):
    def test_empty(self) -> None:
        s = pycom.Signal("s")
        self.assertEqual("s", s.name)
        self.assertFalse(s.value)

    def test_set_value(self) -> None:
        s = pycom.Signal("s")
        self.assertFalse(s.value)
        s.value = True
        self.assertTrue(s.value)

    def test_ctor_component(self) -> None:
        a = pycom.Component("a")
        s = pycom.Signal("s", component=a)
        self.assertIs(s.component, a)
        self.assertSetEqual(a.signals, frozenset({s}))

    def test_set_component(self) -> None:
        a = pycom.Component("a")
        s = pycom.Signal("s")
        s.component = a
        self.assertIs(s.component, a)
        self.assertSetEqual(a.signals, frozenset({s}))

    def test_path(self) -> None:
        a = pycom.Component("a")
        s = pycom.Signal("s", component=a)
        self.assertEqual(s.path, "a.s")
