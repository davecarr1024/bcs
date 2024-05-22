import unittest
import pycom


class MemoryTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Memory(pycom.Bus())

    def test_ctor_data(self) -> None:
        m = pycom.Memory(pycom.Bus(), data={1: pycom.Byte(2)})
        self.assertEqual(m.data[1], pycom.Byte(2))

    def test_set_address(self) -> None:
        m = pycom.Memory(pycom.Bus())
        m.address = 0xBEEF
        self.assertEqual(m.address, 0xBEEF)
        self.assertEqual(m.address_high_byte, pycom.Byte(0xBE))
        self.assertEqual(m.address_low_byte, pycom.Byte(0xEF))

    def test_get_value(self) -> None:
        m = pycom.Memory(pycom.Bus(), data={1: pycom.Byte(2)})
        m.address = 1
        self.assertEqual(m.value, pycom.Byte(2))

    def test_set_value(self) -> None:
        m = pycom.Memory(pycom.Bus())
        m.address = 1
        m.value = pycom.Byte(2)
        self.assertEqual(m.value, pycom.Byte(2))
        self.assertDictEqual(m.data, {1: pycom.Byte(2)})

    def test_get_default(self) -> None:
        m = pycom.Memory(pycom.Bus())
        m.address = 1
        self.assertEqual(m.value, pycom.Byte(0))

    def test_address_in(self) -> None:
        bus = pycom.Bus()
        memory = pycom.Memory(bus)
        memory.set_controls("address_high_byte.in")
        bus.value = pycom.Byte(0xBE)
        memory.update()
        memory.set_controls("address_low_byte.in")
        bus.value = pycom.Byte(0xEF)
        memory.update()
        self.assertEqual(memory.address, 0xBEEF)

    def test_data_in(self) -> None:
        bus = pycom.Bus()
        memory = pycom.Memory(bus)
        memory.address = 1
        memory.set_controls("in")
        bus.value = pycom.Byte(2)
        self.assertEqual(memory.value, pycom.Byte(0))
        memory.update()
        self.assertDictEqual(memory.data, {1: pycom.Byte(2)})

    def test_data_out(self) -> None:
        bus = pycom.Bus()
        memory = pycom.Memory(bus, data={1: pycom.Byte(2)})
        memory.address = 1
        memory.set_controls("out")
        self.assertEqual(bus.value, pycom.Byte(2))
        memory.update()
        self.assertEqual(bus.value, pycom.Byte(2))
