import unittest
import pycom


class RelativeTest(unittest.TestCase):
    def test_statement(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.operands.Relative(1).statement(2),
            ),
            pycom.computer.Program().with_values(2, 1),
        )
