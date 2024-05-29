import unittest
import pycom


class InstructionTest(unittest.TestCase):
    def test_status_instance_entries(self) -> None:
        entries = pycom.Instruction.OperandInstance.StatusInstance(
            steps=[
                pycom.Instruction.step("a"),
                pycom.Instruction.step("b"),
            ]
        ).entries(
            opcode=1,
            status_mask=2,
            status_value=3,
        )
        self.assertIn(
            pycom.Controller.Entry(
                instruction=1,
                instruction_counter=len(pycom.Instruction._preamble()),
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
            pycom.Controller.Entry(
                instruction=1,
                instruction_counter=len(pycom.Instruction._preamble()) + 1,
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
            pycom.Instruction.OperandInstance(
                opcode=1,
            ).with_status_instances(
                {
                    pycom.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.Instruction.step("a"),
                        ]
                    )
                },
            ),
            pycom.Instruction.OperandInstance(
                opcode=1,
                status_instances={
                    pycom.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.Instruction.step("a"),
                        ]
                    )
                },
            ),
        )

    def test_operand_instance_with_status_instance(self) -> None:
        self.assertEqual(
            pycom.Instruction.OperandInstance(
                opcode=1,
            ).with_status_instance(
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.Instruction.step("a"),
                ],
            ),
            pycom.Instruction.OperandInstance(
                opcode=1,
                status_instances={
                    pycom.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.Instruction.step("a"),
                        ]
                    )
                },
            ),
        )

    def test_operand_instance_build(self) -> None:
        self.assertEqual(
            pycom.Instruction.OperandInstance.build(
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.Instruction.step("a"),
                ],
            ),
            pycom.Instruction.OperandInstance(
                opcode=1,
                status_instances={
                    pycom.Instruction.OperandInstance.StatusInstanceKey(
                        status_mask=2,
                        status_value=3,
                    ): pycom.Instruction.OperandInstance.StatusInstance(
                        steps=[
                            pycom.Instruction.step("a"),
                        ]
                    )
                },
            ),
        )

    def test_operand_instance_entries(self) -> None:
        self.assertIn(
            pycom.Controller.Entry(
                instruction=1,
                instruction_counter=len(pycom.Instruction._preamble()),
                status_mask=2,
                status_value=3,
                controls=frozenset(
                    {
                        "a",
                        "controller.instruction_counter.reset",
                    }
                ),
            ),
            pycom.Instruction.OperandInstance.build(
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.Instruction.step("a"),
                ],
            ).entries(),
        )

    def test_operand_instance_statement(self) -> None:
        self.assertEqual(
            pycom.Instruction.OperandInstance.build(
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[
                    pycom.Instruction.step("a"),
                ],
            ).statement(pycom.operands.Immediate(4)),
            pycom.operands.Immediate.Statement(
                opcode=1,
                value=4,
            ),
        )

    def test_with_operand_instances(self) -> None:
        self.assertEqual(
            pycom.Instruction().with_operand_instances(
                {
                    pycom.operands.Relative: pycom.Instruction.OperandInstance.build(
                        opcode=1, steps=[]
                    ),
                }
            ),
            pycom.Instruction(
                operand_instances={
                    pycom.operands.Relative: pycom.Instruction.OperandInstance.build(
                        opcode=1, steps=[]
                    ),
                }
            ),
        )

    def test_with_operand_instance(self) -> None:
        self.assertEqual(
            pycom.Instruction().with_operand_instance(
                pycom.operands.Relative,
                pycom.Instruction.OperandInstance.build(opcode=1, steps=[]),
            ),
            pycom.Instruction(
                operand_instances={
                    pycom.operands.Relative: pycom.Instruction.OperandInstance.build(
                        opcode=1, steps=[]
                    ),
                }
            ),
        )

    def test_with_instance(self) -> None:
        self.assertEqual(
            pycom.Instruction().with_instance(
                operand_type=pycom.operands.Relative,
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[pycom.Instruction.step("a")],
            ),
            pycom.Instruction(
                operand_instances={
                    pycom.operands.Relative: pycom.Instruction.OperandInstance.build(
                        opcode=1,
                        status_mask=2,
                        status_value=3,
                        steps=[pycom.Instruction.step("a")],
                    ),
                }
            ),
        )

    def test_build(self) -> None:
        self.assertEqual(
            pycom.Instruction.build(
                operand_type=pycom.operands.Relative,
                opcode=1,
                status_mask=2,
                status_value=3,
                steps=[pycom.Instruction.step("a")],
            ),
            pycom.Instruction(
                operand_instances={
                    pycom.operands.Relative: pycom.Instruction.OperandInstance.build(
                        opcode=1,
                        status_mask=2,
                        status_value=3,
                        steps=[pycom.Instruction.step("a")],
                    ),
                }
            ),
        )
