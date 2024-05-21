import unittest

import pycom


class ROMTest(unittest.TestCase):
    def test_empty(self) -> None:
        rom = pycom.memory.ROM("", 1024)
        self.assertEqual(1024, rom.size)
        self.assertDictEqual(dict(rom), {})

    def test_init(self) -> None:
        self.assertDictEqual(
            dict(pycom.memory.ROM("r", 1024, {1: pycom.Byte(1), 2: pycom.Byte(10)})),
            {1: pycom.Byte(1), 2: pycom.Byte(10)},
        )

    def test_invalid_init(self) -> None:
        with self.assertRaises(pycom.memory.ROM.AddressError):
            pycom.memory.ROM("r", 1024, {-1: pycom.Byte(1)})
        with self.assertRaises(pycom.memory.ROM.AddressError):
            pycom.memory.ROM("r", 1024, {2048: pycom.Byte(1)})

    def test_getitem(self) -> None:
        self.assertEqual(
            pycom.Byte(2),
            pycom.memory.ROM("r", 1024, {1: pycom.Byte(2)})[1],
        )

    def test_getitem_default(self) -> None:
        self.assertEqual(
            pycom.Byte(0),
            pycom.memory.ROM("r", 1024)[1],
        )

    def test_invalid_getitem(self) -> None:
        with self.assertRaises(pycom.memory.ROM.AddressError):
            pycom.memory.ROM("r", 1024)[1024]
