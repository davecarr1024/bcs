import unittest

import pycom


class RegisterTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Register(pycom.Bus(), "a")

    def test_idle(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        bus.value = pycom.Byte(1)
        register.value = pycom.Byte(2)
        register.update()
        self.assertEqual(bus.value, pycom.Byte(1))
        self.assertEqual(register.value, pycom.Byte(2))

    def test_in(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        register.in_ = True
        bus.value = pycom.Byte(1)
        register.value = pycom.Byte(2)
        register.update()
        self.assertEqual(bus.value, pycom.Byte(1))
        self.assertEqual(register.value, pycom.Byte(1))

    def test_out(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        bus.value = pycom.Byte(1)
        register.value = pycom.Byte(2)
        register.out = True
        register.update()
        self.assertEqual(bus.value, pycom.Byte(2))
        self.assertEqual(register.value, pycom.Byte(2))
