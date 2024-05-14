import unittest

import bcs


class BusTest(unittest.TestCase):
    def test_value(self) -> None:
        bus = bcs.components.bus.Bus(4)
        bus.value = 5
        self.assertEqual(bus.value, 5)

    def test_value_out_of_range_truncates(self) -> None:
        bus = bcs.components.bus.Bus(4)
        bus.value = 0x1F
        self.assertEqual(bus.value, 0xF)
