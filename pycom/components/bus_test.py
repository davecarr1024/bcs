import unittest

import pycom


class BusTest(unittest.TestCase):
    def test_set(self) -> None:
        bus = pycom.Bus(0)
        self.assertEqual(0, bus.value)
        bus.value = 1
        self.assertEqual(1, bus.value)
