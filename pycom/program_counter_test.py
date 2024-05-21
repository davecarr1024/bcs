import unittest

import pycom


class ProgramCounterTest(unittest.TestCase):
    def test_counter_mode_enabled_carry(self) -> None:
        bus = pycom.Bus()
        pc = pycom.ProgramCounter(bus)
        pc.low_byte = pycom.Byte(pycom.Byte.max() - 1)
        pc.high_byte = pycom.Byte(0)
        pc.counter_mode = pycom.ProgramCounter.CounterMode.ENABLED
        pc.tick()
        self.assertEqual(pc.low_byte, pycom.Byte(0))
        self.assertEqual(pc.high_byte, pycom.Byte(1))

    def test_counter_mode_enabled(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.low_byte = pycom.Byte(1)
        pc.high_byte = pycom.Byte(2)
        pc.counter_mode = pycom.ProgramCounter.CounterMode.ENABLED
        pc.tick()
        self.assertEqual(pc.low_byte, pycom.Byte(2))
        self.assertEqual(pc.high_byte, pycom.Byte(2))

    def test_counter_mode_disabled(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.low_byte = pycom.Byte(1)
        pc.high_byte = pycom.Byte(2)
        pc.counter_mode = pycom.ProgramCounter.CounterMode.DISABLED
        pc.tick()
        self.assertEqual(pc.low_byte, pycom.Byte(1))
        self.assertEqual(pc.high_byte, pycom.Byte(2))

    def test_counter_mode_reset(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.low_byte = pycom.Byte(1)
        pc.high_byte = pycom.Byte(2)
        pc.counter_mode = pycom.ProgramCounter.CounterMode.RESET
        pc.tick()
        self.assertEqual(pc.low_byte, pycom.Byte(0))
        self.assertEqual(pc.high_byte, pycom.Byte(0))

    def test_action(self) -> None:
        for action, data_mode, counter_mode in list[
            tuple[
                pycom.ProgramCounter.Action,
                pycom.ProgramCounter.DataMode,
                pycom.ProgramCounter.CounterMode,
            ]
        ](
            [
                (
                    pycom.ProgramCounter.SetDataMode(
                        "", pycom.ProgramCounter.DataMode.IDLE
                    ),
                    pycom.ProgramCounter.DataMode.IDLE,
                    pycom.ProgramCounter.CounterMode.DISABLED,
                ),
                (
                    pycom.ProgramCounter.SetDataMode(
                        "", pycom.ProgramCounter.DataMode.READ_LOW_BYTE
                    ),
                    pycom.ProgramCounter.DataMode.READ_LOW_BYTE,
                    pycom.ProgramCounter.CounterMode.DISABLED,
                ),
                (
                    pycom.ProgramCounter.SetDataMode(
                        "", pycom.ProgramCounter.DataMode.READ_HIGH_BYTE
                    ),
                    pycom.ProgramCounter.DataMode.READ_HIGH_BYTE,
                    pycom.ProgramCounter.CounterMode.DISABLED,
                ),
                (
                    pycom.ProgramCounter.SetDataMode(
                        "", pycom.ProgramCounter.DataMode.WRITE_LOW_BYTE
                    ),
                    pycom.ProgramCounter.DataMode.WRITE_LOW_BYTE,
                    pycom.ProgramCounter.CounterMode.DISABLED,
                ),
                (
                    pycom.ProgramCounter.SetDataMode(
                        "", pycom.ProgramCounter.DataMode.WRITE_HIGH_BYTE
                    ),
                    pycom.ProgramCounter.DataMode.WRITE_HIGH_BYTE,
                    pycom.ProgramCounter.CounterMode.DISABLED,
                ),
                (
                    pycom.ProgramCounter.SetCounterMode(
                        "", pycom.ProgramCounter.CounterMode.DISABLED
                    ),
                    pycom.ProgramCounter.DataMode.IDLE,
                    pycom.ProgramCounter.CounterMode.DISABLED,
                ),
                (
                    pycom.ProgramCounter.SetCounterMode(
                        "", pycom.ProgramCounter.CounterMode.ENABLED
                    ),
                    pycom.ProgramCounter.DataMode.IDLE,
                    pycom.ProgramCounter.CounterMode.ENABLED,
                ),
                (
                    pycom.ProgramCounter.SetCounterMode(
                        "", pycom.ProgramCounter.CounterMode.RESET
                    ),
                    pycom.ProgramCounter.DataMode.IDLE,
                    pycom.ProgramCounter.CounterMode.RESET,
                ),
            ]
        ):
            with self.subTest(
                action=action, data_mode=data_mode, counter_mode=counter_mode
            ):
                pc = pycom.ProgramCounter(pycom.Bus())
                pc.apply(action)
                self.assertEqual(pc.data_mode, data_mode)
                self.assertEqual(pc.counter_mode, counter_mode)

    def test_set_value(self) -> None:
        pc = pycom.ProgramCounter(pycom.Bus())
        pc.value = 0xBEEF
        self.assertEqual(pc.value, 0xBEEF)
        self.assertEqual(pc.low_byte.value, 0xEF)
        self.assertEqual(pc.high_byte.value, 0xBE)
