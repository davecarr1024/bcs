import typing
import unittest
import pycom


class InstructionsTest(unittest.TestCase):
    def test_call(self) -> None:
        for instructions, operand, expected in list[
            tuple[
                pycom.Instructions,
                typing.Optional[pycom.operands.Operand],
                pycom.Statement,
            ]
        ](
            [
                (
                    pycom.Instructions.NOP,
                    None,
                    pycom.operands.None_.Statement(
                        opcode=pycom.Instructions.NOP.value.operand_instance(
                            pycom.operands.None_
                        ).opcode,
                    ),
                ),
                (
                    pycom.Instructions.NOP,
                    pycom.operands.None_(),
                    pycom.operands.None_.Statement(
                        opcode=pycom.Instructions.NOP.value.operand_instance(
                            pycom.operands.None_
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
