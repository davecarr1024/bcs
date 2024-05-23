import unittest

import pycom


class FlagTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Flag("f")

    def test_set_value(self) -> None:
        f = pycom.Flag("f")
        f.value = True
        self.assertTrue(f.value)
        f.value = False
        self.assertFalse(f.value)

    def test_enable_direct(self) -> None:
        f = pycom.Flag("f")
        f.value = False
        f.enable = True
        self.assertTrue(f.value)

    def test_enable_control(self) -> None:
        f = pycom.Flag("f")
        f.value = False
        f.set_controls("enable")
        self.assertTrue(f.value)

    def test_disable_direct(self) -> None:
        f = pycom.Flag("f")
        f.value = True
        f.disable = True
        self.assertFalse(f.value)

    def test_disable_control(self) -> None:
        f = pycom.Flag("f")
        f.value = True
        f.set_controls("disable")
        self.assertFalse(f.value)
