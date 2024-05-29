import unittest
import pycom


class RegisterTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Register(pycom.Bus(), "a")

    def test_ctor_value(self) -> None:
        self.assertEqual(
            pycom.Register(pycom.Bus(), "a", value=1).value,
            1,
        )

    def test_set_value(self) -> None:
        register = pycom.Register(pycom.Bus(), "a")
        register.value = 2
        self.assertEqual(register.value, 2)

    def test_idle(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        bus.value = 1
        register.value = 2
        register.tick()
        self.assertEqual(bus.value, 1)
        self.assertEqual(register.value, 2)

    def test_in(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        register.in_ = True
        bus.value = 1
        register.value = 2
        self.assertEqual(bus.value, 1)
        self.assertEqual(register.value, 2)
        register.tick()
        self.assertEqual(bus.value, 1)
        self.assertEqual(register.value, 1)

    def test_out(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        bus.value = 1
        register.value = 2
        register.out = True
        self.assertEqual(bus.value, 2)
        self.assertEqual(register.value, 2)
        register.tick()
        self.assertEqual(bus.value, 2)
        self.assertEqual(register.value, 2)

    def test_in_and_out(self) -> None:
        bus = pycom.Bus()
        register = pycom.Register(bus, "a")
        bus.value = 1
        register.value = 2
        register.in_ = True
        register.out = True
        self.assertEqual(bus.value, 2)
        self.assertEqual(register.value, 2)
        register.tick()
        self.assertEqual(bus.value, 2)
        self.assertEqual(register.value, 2)
