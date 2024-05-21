import unittest

import pycom


class ControlTest(unittest.TestCase):
    def test_empty(self) -> None:
        c = pycom.Control("c")
        self.assertEqual("c", c.name)
        self.assertFalse(c.value)

    def test_set_value(self) -> None:
        c = pycom.Control("c")
        self.assertFalse(c.value)
        c.value = True
        self.assertTrue(c.value)

    def test_onchange(self) -> None:
        on_change_value = False

        def on_change(value: bool) -> None:
            nonlocal on_change_value
            on_change_value = value

        c = pycom.Control("c", on_change)
        c.value = True
        self.assertTrue(on_change_value)
        c.value = False
        self.assertFalse(on_change_value)
