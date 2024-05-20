import unittest

import pycom


class ComputerTest(unittest.TestCase):
    def test_transfer_register(self) -> None:
        bus = pycom.Bus()
        a = pycom.Register(bus, "a")
        b = pycom.Register(bus, "b")
        c = pycom.Computer(a, b)
        a.value = pycom.Byte(1)
        b.value = pycom.Byte(2)
        c.apply(
            [
                pycom.Register.SetDataMode("a", pycom.Register.DataMode.WRITE),
                pycom.Register.SetDataMode("b", pycom.Register.DataMode.READ),
            ]
        )
        c.update()
        self.assertEqual(a.value, pycom.Byte(1))
        self.assertEqual(b.value, pycom.Byte(1))
