import unittest

import pycom


class OperationTest(unittest.TestCase):
    def test_call_empty(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.Operation(
                    instruction=pycom.computer.Instructions.NOP,
                )
            ),
            pycom.computer.Program(
                data={
                    0: pycom.computer.Instructions.NOP.value.opcode,
                },
                next_address=1,
            ),
        )

    def test_call_int_operand(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_statement(
                pycom.computer.Operation(
                    instruction=pycom.computer.Instructions.NOP,
                    operands=[1],
                )
            ),
            pycom.computer.Program(
                data={
                    0: pycom.computer.Instructions.NOP.value.opcode,
                    1: 1,
                },
                next_address=2,
            ),
        )

    def test_call_str_operand(self) -> None:
        self.assertEqual(
            pycom.computer.Program(
                labels={"a": 0xBEEF},
            ).with_statement(
                pycom.computer.Operation(
                    instruction=pycom.computer.Instructions.NOP,
                    operands=["a"],
                )
            ),
            pycom.computer.Program(
                labels={"a": 0xBEEF},
                data={
                    0: pycom.computer.Instructions.NOP.value.opcode,
                    1: 0xBE,
                    2: 0xEF,
                },
                next_address=3,
            ),
        )

    def test_call_str_operand_not_found(self) -> None:
        with self.assertRaises(pycom.computer.Program.LabelNotFoundError):
            pycom.computer.Program().with_statement(
                pycom.computer.Operation(
                    instruction=pycom.computer.Instructions.NOP,
                    operands=["a"],
                )
            )

    def test_call_multiple_operands(self) -> None:
        self.assertEqual(
            pycom.computer.Program(
                labels={"a": 0xBEEF},
            ).with_statement(
                pycom.computer.Operation(
                    instruction=pycom.computer.Instructions.NOP,
                    operands=[
                        1,
                        2,
                        "a",
                    ],
                )
            ),
            pycom.computer.Program(
                labels={"a": 0xBEEF},
                data={
                    0: pycom.computer.Instructions.NOP.value.opcode,
                    1: 1,
                    2: 2,
                    3: 0xBE,
                    4: 0xEF,
                },
                next_address=5,
            ),
        )
