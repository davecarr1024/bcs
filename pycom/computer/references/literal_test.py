import unittest
import pycom


class LiteralTest(unittest.TestCase):
    def test_call(self) -> None:
        program = pycom.computer.Program()
        self.assertEqual(
            pycom.computer.references.Literal(1)(
                pycom.computer.Program.Output(
                    program,
                ),
                0,
            ),
            pycom.computer.Program.Output(program).with_value_at(0, 1),
        )

    def test_size(self) -> None:
        self.assertEqual(
            pycom.computer.references.Literal.size(),
            1,
        )
