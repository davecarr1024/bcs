import unittest
import pycom


class LiteralTest(unittest.TestCase):
    def test_call(self) -> None:
        program = pycom.Program()
        self.assertEqual(
            pycom.references.Literal(1)(
                pycom.Program.Output(
                    program,
                ),
                0,
            ),
            pycom.Program.Output(program).with_value_at(0, 1),
        )

    def test_size(self) -> None:
        self.assertEqual(
            pycom.references.Literal.size(),
            1,
        )
