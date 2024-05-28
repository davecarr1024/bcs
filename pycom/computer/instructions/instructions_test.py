import typing
import unittest
import pycom


class InstructionsTest(unittest.TestCase):
    def test_call(self) -> None:
        for instructions, operand, expected in list[
            tuple[
                pycom.computer.Instructions,
                typing.Optional[pycom.computer.operands.Operand],
                pycom.computer.Statement,
            ]
        ](
            [
                (
                    pycom.computer.Instructions.NOP,
                    None,
                    pycom.computer.operands.None_.Statement(
                        opcode=pycom.computer.Instructions.NOP.value.operand_instance(
                            pycom.computer.operands.None_
                        ).opcode,
                    ),
                ),
                (
                    pycom.computer.Instructions.NOP,
                    pycom.computer.operands.None_(),
                    pycom.computer.operands.None_.Statement(
                        opcode=pycom.computer.Instructions.NOP.value.operand_instance(
                            pycom.computer.operands.None_
                        ).opcode,
                    ),
                ),
            ]
        ):
            with self.subTest(
                instructions=instructions,
                operand=operand,
                expected=expected,
            ):
                if operand is not None:
                    self.assertEqual(
                        instructions(operand),
                        expected,
                    )
                else:
                    self.assertEqual(
                        instructions(),
                        expected,
                    )
