import unittest

import pycom


class RAMTest(unittest.TestCase):
    def test_setitem(self) -> None:
        ram = pycom.memory.RAM("r", 1024)
        ram[1] = pycom.Byte(2)
        self.assertDictEqual(
            dict(ram),
            {1: pycom.Byte(2)},
        )

    def test_setitem_invalid(self) -> None:
        with self.assertRaises(pycom.memory.RAM.AddressError):
            pycom.memory.RAM("r", 1024)[1024] = pycom.Byte(1)

    def test_delitem(self) -> None:
        ram = pycom.memory.RAM("r", 1024, {1: pycom.Byte(2)})
        del ram[1]
        self.assertDictEqual(dict(ram), {})

    def test_delitem_invalid(self) -> None:
        with self.assertRaises(pycom.memory.RAM.AddressError):
            del pycom.memory.RAM("r", 1024)[1024]
