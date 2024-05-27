import unittest
import pycom


class InstructionTest(unittest.TestCase):
    def test_nop(self) -> None:
        entries = pycom.computer.Instruction.build(1).entries()
        self.assertEqual(
            len(entries),
            len(pycom.computer.Instruction._preamble()) + 1,
        )
        self.assertIn(
            pycom.Controller.Entry(
                instruction=1,
                instruction_counter=len(pycom.computer.Instruction._preamble()),
                controls=frozenset({"controller.instruction_counter.reset"}),
            ),
            entries,
        )
        self.assertSetEqual(
            {entry.instruction_counter for entry in entries},
            set(
                range(len(entries)),
            ),
        )
