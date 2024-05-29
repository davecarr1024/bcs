import unittest
import pycom


class MemoryTest(unittest.TestCase):
    def test_empty(self) -> None:
        pycom.Memory(pycom.Bus())

    def test_ctor_data(self) -> None:
        m = pycom.Memory(pycom.Bus(), data={1: 2})
        self.assertEqual(m.data[1], 2)

    def test_set_address(self) -> None:
        m = pycom.Memory(pycom.Bus())
        m.address = 0xBEEF
        self.assertEqual(m.address, 0xBEEF)
        self.assertEqual(m.address_high_byte, 0xBE)
        self.assertEqual(m.address_low_byte, 0xEF)

    def test_get_value(self) -> None:
        m = pycom.Memory(pycom.Bus(), data={1: 2})
        m.address = 1
        self.assertEqual(m.value, 2)

    def test_set_value(self) -> None:
        m = pycom.Memory(pycom.Bus())
        m.address = 1
        m.value = 2
        self.assertEqual(m.value, 2)
        self.assertDictEqual(m.data, {1: 2})

    def test_get_default(self) -> None:
        m = pycom.Memory(pycom.Bus())
        m.address = 1
        self.assertEqual(m.value, 0)

    def test_address_in(self) -> None:
        bus = pycom.Bus()
        memory = pycom.Memory(bus)
        memory.set_controls("address_high_byte.in")
        bus.value = 0xBE
        memory.tick()
        memory.set_controls("address_low_byte.in")
        bus.value = 0xEF
        memory.tick()
        self.assertEqual(memory.address, 0xBEEF)

    def test_data_in(self) -> None:
        bus = pycom.Bus()
        memory = pycom.Memory(bus)
        memory.address = 1
        memory.set_controls("in")
        bus.value = 2
        self.assertEqual(memory.value, 0)
        memory.tick()
        self.assertDictEqual(memory.data, {1: 2})

    def test_data_out(self) -> None:
        bus = pycom.Bus()
        memory = pycom.Memory(bus, data={1: 2})
        memory.address = 1
        memory.set_controls("out")
        self.assertEqual(bus.value, 2)
        memory.tick()
        self.assertEqual(bus.value, 2)

    def test_get_item(self) -> None:
        self.assertDictEqual(
            dict(pycom.Memory(pycom.Bus(), data={1: 2})),
            {1: 2},
        )

    def test_set_item(self) -> None:
        memory = pycom.Memory(pycom.Bus())
        memory[1] = 2
        self.assertDictEqual(
            dict(memory),
            {1: 2},
        )
