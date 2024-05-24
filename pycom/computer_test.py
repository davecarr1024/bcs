import unittest

import pycom


class ComputerTest(unittest.TestCase):
    def test_empty(self) -> None:
        computer = pycom.Computer()
        self.assertEqual(computer.program_counter.value, 0)
        self.assertEqual(computer.controller.instruction_counter, pycom.Byte(0))

    def test_nop(self) -> None:
        computer = pycom.Computer()
        self.assertEqual(computer.controller.run_instruction(), 4)
        self.assertEqual(computer.controller.instruction_counter, pycom.Byte(0))
        self.assertEqual(computer.program_counter.value, 1)

    def test_lda_immediate(self) -> None:
        computer = pycom.Computer(
            data={
                0: 1,
                1: 2,
            }
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a.value, 2)

    def test_lda_memory(self) -> None:
        computer = pycom.Computer(
            data={
                0: 2,
                1: 0xBE,
                2: 0xEF,
                0xBEEF: 42,
            }
        )
        computer.controller.run_instruction()
        self.assertEqual(computer.a.value, 42)

    def test_sta_memory(self) -> None:
        computer = pycom.Computer(
            data={
                0: 1,
                1: 42,
                2: 3,
                3: 0xBE,
                4: 0xEF,
            }
        )
        computer.controller.run_instructions(2)
        self.assertEqual(
            computer.memory.data[0xBEEF],
            42,
        )
