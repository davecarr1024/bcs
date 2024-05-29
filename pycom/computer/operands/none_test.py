import unittest
import pycom


class NoneTest(unittest.TestCase):
    def test_statement(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.operands.None_().statement(1),
            ),
            pycom.computer.Program().with_value(
                pycom.computer.references.Literal(1),
            ),
        )
