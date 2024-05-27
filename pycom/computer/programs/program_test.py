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
        for program, value, expected in list[
            tuple[
                pycom.computer.Program,
                pycom.computer.programs.program.Value,
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
                    pycom.computer.Program(),
                    "a",
                    pycom.computer.Program(
                        data={0: "a"},
                        next_address=2,
                    ),
                ),
            ]
        ):
            with self.subTest(
                program=program,
                value=value,
                expected=expected,
            ):
                self.assertEqual(
                    program.with_value(value),
                    expected,
                )

    def test_with_values(self) -> None:
        for program, values, expected in list[
            tuple[
                pycom.computer.Program,
                typing.Iterable[pycom.computer.programs.program.Value],
                pycom.computer.Program,
            ]
        ](
            [
                (
                    pycom.computer.Program(),
                    [],
                    pycom.computer.Program(),
                ),
                (
                    pycom.computer.Program(),
                    [1],
                    pycom.computer.Program(
                        data={0: 1},
                        next_address=1,
                    ),
                ),
                (
                    pycom.computer.Program(),
                    "a",
                    pycom.computer.Program(
                        data={0: "a"},
                        next_address=2,
                    ),
                ),
                (
                    pycom.computer.Program(),
                    [1, "a", 2],
                    pycom.computer.Program(
                        data={
                            0: 1,
                            1: "a",
                            3: 2,
                        },
                        next_address=4,
                    ),
                ),
            ]
        ):
            with self.subTest(
                program=program,
                value=values,
                expected=expected,
            ):
                self.assertEqual(
                    program.with_values(*values),
                    expected,
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

    def test_finalize_data(self) -> None:
        for program, expected in list[
            tuple[
                pycom.computer.Program,
                typing.Optional[typing.Mapping[int, int]],
            ]
        ](
            [
                (
                    pycom.computer.Program(),
                    {},
                ),
                (
                    pycom.computer.Program().with_value(1),
                    {
                        0: 1,
                    },
                ),
                (
                    pycom.computer.Program().with_value("a"),
                    None,
                ),
                (
                    pycom.computer.Program().with_value("a").at(0xBEEF).with_label("a"),
                    {
                        0: 0xBE,
                        1: 0xEF,
                    },
                ),
            ]
        ):
            with self.subTest(
                program=program,
                expected=expected,
            ):
                if expected is None:
                    with self.assertRaises(pycom.computer.Program.Error):
                        program.finalize_data()
                else:
                    self.assertDictEqual(
                        program.finalize_data(),
                        expected,
                    )
