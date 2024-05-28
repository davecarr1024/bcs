import unittest
import pycom


class InstructionTest(unittest.TestCase):
    def test_status_instance_entries(self) -> None:
        entries = pycom.computer.Instruction.OperandInstance.StatusInstance(
            steps=[
                pycom.computer.Instruction.step("a"),
                pycom.computer.Instruction.step("b"),
            ]
        ).entries(
            opcode=1,
            status_mask=2,
            status_value=3,
        )
        self.assertIn(
            pycom.controller.Controller.Entry(
                instruction=1,
                instruction_counter=len(pycom.computer.Instruction._preamble()),
                status_mask=2,
                status_value=3,
                controls=frozenset(
                    {
                        "a",
                        "controller.instruction_counter.increment",
                    }
                ),
            ),
            entries,
        )
        self.assertIn(
            pycom.controller.Controller.Entry(
                instruction=1,
                instruction_counter=len(pycom.computer.Instruction._preamble()) + 1,
                status_mask=2,
                status_value=3,
                controls=frozenset(
                    {
                        "b",
                        "controller.instruction_counter.reset",
                    }
                ),
            ),
            entries,
        )

    def test_operand_instance_with_status_instances(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction.OperandInstance(
                opcode=1,
            ).with_status_instances(
                {
                    pycom.computer.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.computer.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.computer.Instruction.step("a"),
                        ]
                    )
                },
            ),
            pycom.computer.Instruction.OperandInstance(
                opcode=1,
                status_instances={
                    pycom.computer.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.computer.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.computer.Instruction.step("a"),
                        ]
                    )
                },
            ),
        )

    def test_operand_instance_with_status_instance(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction.OperandInstance(
                opcode=1,
            ).with_status_instance(
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.computer.Instruction.step("a"),
                ],
            ),
            pycom.computer.Instruction.OperandInstance(
                opcode=1,
                status_instances={
                    pycom.computer.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.computer.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.computer.Instruction.step("a"),
                        ]
                    )
                },
            ),
        )

    def test_operand_instance_build(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction.OperandInstance.build(
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.computer.Instruction.step("a"),
                ],
            ),
            pycom.computer.Instruction.OperandInstance(
                opcode=1,
                status_instances={
                    pycom.computer.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.computer.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.computer.Instruction.step("a"),
                        ]
                    )
                },
            ),
        )

    def test_operand_instance_entries(self) -> None:
        self.assertIn(
            pycom.controller.Controller.Entry(
                instruction=1,
                instruction_counter=len(pycom.computer.Instruction._preamble()),
                status_mask=2,
                status_value=3,
                controls=frozenset(
                    {
                        "a",
                        "controller.instruction_counter.reset",
                    }
                ),
            ),
            pycom.computer.Instruction.OperandInstance.build(
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.computer.Instruction.step("a"),
                ],
            ).entries(),
        )

    def test_operand_instance_statement(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction.OperandInstance.build(
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.computer.Instruction.step("a"),
                ],
            ).statement(pycom.computer.operands.Immediate(4)),
            pycom.computer.operands.Immediate.Statement(
                opcode=1,
                value=4,
            ),
        )

    def test_with_operand_instances(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction().with_operand_instances(
                {
                    pycom.computer.operands.Relative: pycom.computer.Instruction.OperandInstance.build(
                        opcode=1, steps=[]
                    ),
                }
            ),
            pycom.computer.Instruction(
                operand_instances={
                    pycom.computer.operands.Relative: pycom.computer.Instruction.OperandInstance.build(
                        opcode=1, steps=[]
                    ),
                }
            ),
        )

    def test_with_operand_instance(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction().with_operand_instance(
                pycom.computer.operands.Relative,
                pycom.computer.Instruction.OperandInstance.build(opcode=1, steps=[]),
            ),
            pycom.computer.Instruction(
                operand_instances={
                    pycom.computer.operands.Relative: pycom.computer.Instruction.OperandInstance.build(
                        opcode=1, steps=[]
                    ),
                }
            ),
        )

    def test_with_instance(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction().with_instance(
                operand_type=pycom.computer.operands.Relative,
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[pycom.computer.Instruction.step("a")],
            ),
            pycom.computer.Instruction(
                operand_instances={
                    pycom.computer.operands.Relative: pycom.computer.Instruction.OperandInstance.build(
                        opcode=1,
                        status_mask=2,
                        status_value=3,
                        steps=[pycom.computer.Instruction.step("a")],
                    ),
                }
            ),
        )

    def test_build(self) -> None:
        self.assertEqual(
            pycom.computer.Instruction.build(
                operand_type=pycom.computer.operands.Relative,
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[pycom.computer.Instruction.step("a")],
            ),
            pycom.computer.Instruction(
                operand_instances={
                    pycom.computer.operands.Relative: pycom.computer.Instruction.OperandInstance.build(
                        opcode=1,
                        status_mask=2,
                        status_value=3,
                        steps=[pycom.computer.Instruction.step("a")],
                    ),
                }
            ),
        )
