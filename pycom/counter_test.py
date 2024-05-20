import unittest

import pycom


class CounterTest(unittest.TestCase):
    def test_apply_set_counter_mode(self) -> None:
        bus = pycom.Bus()
        counter = pycom.Counter(bus, "a")
        counter.counter_mode = pycom.Counter.CounterMode.DISABLED
        counter.apply(
            pycom.Counter.SetCounterMode("a", pycom.Counter.CounterMode.ENABLED)
        )
        self.assertEqual(counter.counter_mode, pycom.Counter.CounterMode.ENABLED)

    def test_apply_set_data_mode(self) -> None:
        bus = pycom.Bus()
        counter = pycom.Counter(bus, "a")
        counter.data_mode = pycom.Counter.DataMode.IDLE
        counter.apply(pycom.Counter.SetDataMode("a", pycom.Counter.DataMode.READ))
        self.assertEqual(pycom.Counter.DataMode.READ, counter.data_mode)

    def test_disabled(self) -> None:
        bus = pycom.Bus()
        counter = pycom.Counter(bus, "a")
        counter.counter_mode = pycom.Counter.CounterMode.DISABLED
        counter.value = pycom.Byte(1)
        counter.update()
        self.assertEqual(pycom.Byte(1), counter.value)

    def test_enabled(self) -> None:
        bus = pycom.Bus()
        counter = pycom.Counter(bus, "a")
        counter.counter_mode = pycom.Counter.CounterMode.ENABLED
        counter.value = pycom.Byte(1)
        counter.update()
        self.assertEqual(pycom.Byte(2), counter.value)

    def test_reset(self) -> None:
        bus = pycom.Bus()
        counter = pycom.Counter(bus, "a")
        counter.counter_mode = pycom.Counter.CounterMode.RESET
        counter.value = pycom.Byte(1)
        counter.update()
        self.assertEqual(pycom.Byte(0), counter.value)
