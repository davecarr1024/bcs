import unittest

import pycom


class OperationTest(unittest.TestCase):
    def test_call(self) -> None:
        for program, operation, expected in list[
            tuple[
                pycom.computer.Program,
                pycom.computer.Operation,
                pycom.computer.Program,
            ]
        ](
            [
                (
                    pycom.computer.Program(),
                    pycom.computer.Operation(
                        instruction=pycom.computer.Instructions.NOP,
                    ),
                    pycom.computer.Program(
                        data={
                            0: pycom.computer.Instructions.NOP.value.opcode,
                        },
                        next_address=1,
                    ),
                ),
                (
                    pycom.computer.Program(),
                    pycom.computer.Operation(
                        instruction=pycom.computer.Instructions.NOP,
                        operands=[1],
                    ),
                    pycom.computer.Program(
                        data={
                            0: pycom.computer.Instructions.NOP.value.opcode,
                            1: 1,
                        },
                        next_address=2,
                    ),
                ),
                (
                    pycom.computer.Program(),
                    pycom.computer.Operation(
                        instruction=pycom.computer.Instructions.NOP,
                        operands=["a"],
                    ),
                    pycom.computer.Program(
                        data={
                            0: pycom.computer.Instructions.NOP.value.opcode,
                            1: "a",
                        },
                        next_address=3,
                    ),
                ),
                (
                    pycom.computer.Program(),
                    pycom.computer.Operation(
                        instruction=pycom.computer.Instructions.NOP,
                        operands=[1, "a", 2],
                    ),
                    pycom.computer.Program(
                        data={
                            0: pycom.computer.Instructions.NOP.value.opcode,
                            1: 1,
                            2: "a",
                            4: 2,
                        },
                        next_address=5,
                    ),
                ),
            ]
        ):
            with self.subTest(
                program=program,
                operation=operation,
                expected=expected,
            ):
                self.assertEqual(
                    program.with_statement(operation),
                    expected,
                )
