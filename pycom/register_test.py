import unittest

import pycom


class RegisterTest(unittest.TestCase):
    def test_idle(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        register.data_mode = pycom.Register.DataMode.IDLE
        bus.value = pycom.Byte(1)
        register.value = pycom.Byte(2)
        register.update()
        self.assertEqual(bus.value, pycom.Byte(1))
        self.assertEqual(register.value, pycom.Byte(2))

    def test_read(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        register.data_mode = pycom.Register.DataMode.READ
        bus.value = pycom.Byte(1)
        register.value = pycom.Byte(2)
        register.update()
        self.assertEqual(bus.value, pycom.Byte(1))
        self.assertEqual(register.value, pycom.Byte(1))

    def test_write(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        bus.value = pycom.Byte(1)
        register.value = pycom.Byte(2)
        register.data_mode = pycom.Register.DataMode.WRITE
        register.update()
        self.assertEqual(bus.value, pycom.Byte(2))
        self.assertEqual(register.value, pycom.Byte(2))

    def test_apply_set_data_mode(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        register.data_mode = pycom.Register.DataMode.IDLE
        register.apply(pycom.Register.SetDataMode("a", pycom.Register.DataMode.READ))
        self.assertEqual(pycom.Register.DataMode.READ, register.data_mode)
