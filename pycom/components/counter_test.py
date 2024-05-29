import unittest

import pycom


class CounterTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Counter(pycom.Bus(), "c")

    def test_idle(self) -> None:
        c = pycom.Counter(pycom.Bus(), "c", value=1)
        c.update()
        self.assertEqual(c.value, pycom.Byte(1))

    def test_increment(self) -> None:
        c = pycom.Counter(pycom.Bus(), "c", value=1)
        c.increment = True
        c.update()
        self.assertEqual(c.value, pycom.Byte(2))

    def test_reset(self) -> None:
        c = pycom.Counter(pycom.Bus(), "c", value=1)
        c.reset = True
        c.update()
        self.assertEqual(c.value, pycom.Byte(0))
