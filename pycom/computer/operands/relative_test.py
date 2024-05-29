import unittest
import pycom


class RelativeTest(unittest.TestCase):
    def test_statement_literal(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.operands.Relative(1).statement(2),
            ),
            pycom.computer.Program().with_values(
                pycom.computer.references.Literal(2),
                pycom.computer.references.Literal(1),
            ),
        )

    def test_statement_label(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.operands.Relative("a").statement(2),
            ),
            pycom.computer.Program().with_values(
                pycom.computer.references.Literal(2),
                pycom.computer.references.Relative("a"),
            ),
        )
