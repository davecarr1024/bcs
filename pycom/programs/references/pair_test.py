import unittest
import pycom


class PairTest(unittest.TestCase):
    def test_call(self) -> None:
        program = pycom.Program()
        self.assertEqual(
            pycom.references.Pair(1, 2)(
                pycom.Program.Output(
                    program,
                ),
                0,
            ),
            pycom.Program.Output(program).with_values_at(0, 1, 2),
        )

    def test_size(self) -> None:
        self.assertEqual(
            pycom.references.Pair.size(),
            2,
        )
