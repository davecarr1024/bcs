import unittest

import pycom


class ProgramCounterTest(unittest.TestCase):
    def test_idle(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.low_byte = 1
        pc.high_byte = 2
        pc.update()
        self.assertEqual(pc.low_byte, 1)
        self.assertEqual(pc.high_byte, 2)

    def test_increment(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.low_byte = 1
        pc.high_byte = 2
        pc.increment = True
        pc.update()
        self.assertEqual(pc.low_byte, 2)
        self.assertEqual(pc.high_byte, 2)

    def test_increment_carry(self) -> None:
        bus = pycom.Bus()
        pc = pycom.ProgramCounter(bus)
        pc.low_byte = pycom.Byte.max() - 1
        pc.high_byte = 0
        pc.increment = True
        pc.update()
        self.assertEqual(pc.low_byte, 0)
        self.assertEqual(pc.high_byte, 1)

    def test_reset(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.low_byte = 1
        pc.high_byte = 2
        pc.reset = True
        pc.update()
        self.assertEqual(pc.low_byte, 0)
        self.assertEqual(pc.high_byte, 0)

    def test_set_value(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.value = 0xBEEF
        self.assertEqual(pc.value, 0xBEEF)
        self.assertEqual(pc.low_byte, 0xEF)
        self.assertEqual(pc.high_byte, 0xBE)
