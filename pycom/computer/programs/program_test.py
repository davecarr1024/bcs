import dataclasses
import typing
import unittest
import pycom


class ProgramTest(unittest.TestCase):
    @dataclasses.dataclass(frozen=True)
    class TestStatement(pycom.computer.Statement):
        label: str

        @typing.override
        def __call__(self, program: pycom.computer.Program) -> pycom.computer.Program:
            return program.at(self.label)

    def test_with_data(self) -> None:
        self.assertEqual(
            pycom.computer.Program(data={1: 2}).with_(data={3: 4}),
            pycom.computer.Program(data={1: 2, 3: 4}),
        )

    def test_with_labels(self) -> None:
        self.assertEqual(
            pycom.computer.Program(
                labels={"a": 1},
                data={3: 4},
                next_address=5,
            ).with_(labels={"b": 2}),
            pycom.computer.Program(
                labels={"a": 1, "b": 2},
                data={3: 4},
                next_address=5,
            ),
        )

    def test_with_next_address(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_(next_address=1),
            pycom.computer.Program(next_address=1),
        )

    def test_at(self) -> None:
        self.assertEqual(
            pycom.computer.Program().at(1),
            pycom.computer.Program(next_address=1),
        )

    def test_at_label(self) -> None:
        self.assertEqual(
            pycom.computer.Program(labels={"a": 1}).at("a"),
            pycom.computer.Program(labels={"a": 1}, next_address=1),
        )

    def test_with_value_at(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_value_at(1, 2),
            pycom.computer.Program(data={1: 2}),
        )

    def test_with_value(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_value(1),
            pycom.computer.Program(
                data={0: 1},
                next_address=1,
            ),
        )

    def test_with_values(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_values(1, 2),
            pycom.computer.Program(data={0: 1, 1: 2}, next_address=2),
        )

    def test_with_label_at(self) -> None:
        self.assertEqual(
            pycom.computer.Program().with_label_at("a", 1),
            pycom.computer.Program(labels={"a": 1}),
        )

    def test_with_label(self) -> None:
        self.assertEqual(
            pycom.computer.Program(next_address=1).with_label("a"),
            pycom.computer.Program(
                next_address=1,
                labels={"a": 1},
            ),
        )

    def test_label(self) -> None:
        self.assertEqual(
            pycom.computer.Program(
                labels={"a": 1},
            ).label("a"),
            1,
        )

    def test_label_not_found(self) -> None:
        with self.assertRaises(pycom.computer.Program.LabelNotFoundError):
            pycom.computer.Program().label("a")

    def test_with_statement(self) -> None:
        self.assertEqual(
            pycom.computer.Program(labels={"a": 1}).with_statement(
                self.TestStatement("a")
            ),
            pycom.computer.Program(
                labels={"a": 1},
                next_address=1,
            ),
        )

    def test_with_entry(self) -> None:
        for program, entry, expected in list[
            tuple[
                pycom.computer.Program,
                pycom.computer.programs.program.Entry,
                pycom.computer.Program,
            ]
        ](
            [
                (
                    pycom.computer.Program(),
                    1,
                    pycom.computer.Program(
                        data={0: 1},
                        next_address=1,
                    ),
                ),
                (
                    pycom.computer.Program(
                        next_address=1,
                    ),
                    "a",
                    pycom.computer.Program(
                        labels={"a": 1},
                        next_address=1,
                    ),
                ),
                (
                    pycom.computer.Program(),
                    pycom.computer.Instructions.NOP,
                    pycom.computer.Program(
                        data={
                            0: pycom.computer.Instructions.NOP.value.opcode,
                        },
                        next_address=1,
                    ),
                ),
                (
                    pycom.computer.Program(
                        labels={"a": 1},
                    ),
                    self.TestStatement("a"),
                    pycom.computer.Program(
                        labels={"a": 1},
                        next_address=1,
                    ),
                ),
            ]
        ):
            with self.subTest(
                program=program,
                entry=entry,
                expected=expected,
            ):
                self.assertEqual(
                    program.with_entry(entry),
                    expected,
                )
