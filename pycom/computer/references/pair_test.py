import unittest
import pycom


class PairTest(unittest.TestCase):
    def test_call(self) -> None:
        program = pycom.computer.Program()
        self.assertEqual(
            pycom.computer.references.Pair(1, 2)(
                pycom.computer.Program.Output(
                    program,
                ),
                0,
            ),
            pycom.computer.Program.Output(program).with_values_at(0, 1, 2),
        )

    def test_size(self) -> None:
        self.assertEqual(
            pycom.computer.references.Pair.size(),
            2,
        )
