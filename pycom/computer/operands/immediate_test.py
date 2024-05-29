import unittest
import pycom


class ImmediateTest(unittest.TestCase):
    def test_statement(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.operands.Immediate(1).statement(2),
            ),
            pycom.computer.Program().with_values(
                pycom.computer.references.Literal(2),
                pycom.computer.references.Literal(1),
            ),
        )
