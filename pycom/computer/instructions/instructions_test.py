import typing
import unittest
import pycom


class InstructionsTest(unittest.TestCase):
    def test_call(self) -> None:
        for instructions, operands, expected in list[
            tuple[
                pycom.computer.Instructions,
                typing.Iterable[int | str],
                pycom.computer.Statement,
            ]
        ](
            [
                (
                    pycom.computer.Instructions.NOP,
                    [],
                    pycom.computer.Operation(
                        instruction=pycom.computer.Instructions.NOP,
                    ),
                ),
                (
                    pycom.computer.Instructions.NOP,
                    [
                        1,
                        "a",
                    ],
                    pycom.computer.Operation(
                        instruction=pycom.computer.Instructions.NOP,
                        operands=[
                            1,
                            "a",
                        ],
                    ),
                ),
            ]
        ):
            with self.subTest(
                instructions=instructions,
                operands=operands,
                expected=expected,
            ):
                self.assertEqual(
                    instructions(*operands),
                    expected,
                )
