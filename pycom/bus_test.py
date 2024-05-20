import unittest

import pycom


class BusTest(unittest.TestCase):
    def test_set(self) -> None:
        bus = pycom.bus.Bus()
        self.assertEqual(pycom.Byte(0), bus.value)
        bus.value = pycom.Byte(1)
        self.assertEqual(pycom.Byte(1), bus.value)
