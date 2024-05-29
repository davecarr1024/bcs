import dataclasses
import typing
import unittest
import pycom


class ProgramTest(unittest.TestCase):
    @dataclasses.dataclass(frozen=True)
    class TestStatement(pycom.Statement):
        label: str

        @typing.override
        def __call__(self, program: pycom.Program) -> pycom.Program:
            return program.at(self.label)

    def test_with_data(self) -> None:
        self.assertEqual(
            pycom.Program(
                data={
                    1: pycom.references.Literal(2),
                }
            ).with_(
                data={
                    3: pycom.references.Literal(4),
                }
            ),
            pycom.Program(
                data={
                    1: pycom.references.Literal(2),
                    3: pycom.references.Literal(4),
                }
            ),
        )

    def test_with_labels(self) -> None:
        self.assertEqual(
            pycom.Program(
                labels={"a": 1},
                data={
                    3: pycom.references.Literal(4),
                },
                next_address=5,
            ).with_(labels={"b": 2}),
            pycom.Program(
                labels={"a": 1, "b": 2},
                data={
                    3: pycom.references.Literal(4),
                },
                next_address=5,
            ),
        )

    def test_with_next_address(self) -> None:
        self.assertEqual(
            pycom.Program().with_(next_address=1),
            pycom.Program(next_address=1),
        )

    def test_at(self) -> None:
        self.assertEqual(
            pycom.Program().at(1),
            pycom.Program(next_address=1),
        )

    def test_at_label(self) -> None:
        self.assertEqual(
            pycom.Program(labels={"a": 1}).at("a"),
            pycom.Program(labels={"a": 1}, next_address=1),
        )

    def test_with_value_at(self) -> None:
        self.assertEqual(
            pycom.Program().with_value_at(
                1,
                pycom.references.Literal(2),
            ),
            pycom.Program(
                data={
                    1: pycom.references.Literal(2),
                }
            ),
        )

    def test_with_value(self) -> None:
        for program, value, expected in list[
            tuple[
                pycom.Program,
                pycom.references.Reference,
                pycom.Program,
            ]
        ](
            [
                (
                    pycom.Program(),
                    pycom.references.Literal(1),
                    pycom.Program(
                        data={0: pycom.references.Literal(1)},
                        next_address=1,
                    ),
                ),
                (
                    pycom.Program(),
                    pycom.references.Pair(1, 2),
                    pycom.Program(
                        data={0: pycom.references.Pair(1, 2)},
                        next_address=2,
                    ),
                ),
                (
                    pycom.Program(),
                    pycom.references.Absolute("a"),
                    pycom.Program(
                        data={
                            0: pycom.references.Absolute("a"),
                        },
                        next_address=2,
                    ),
                ),
                (
                    pycom.Program(),
                    pycom.references.Relative("a"),
                    pycom.Program(
                        data={
                            0: pycom.references.Relative("a"),
                        },
                        next_address=1,
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

    # def test_with_values(self) -> None:
    #     for program, values, expected in list[
    #         tuple[
    #             pycom.Program,
    #             typing.Iterable[pycom.Programs.program.Value],
    #             pycom.Program,
    #         ]
    #     ](
    #         [
    #             (
    #                 pycom.Program(),
    #                 [],
    #                 pycom.Program(),
    #             ),
    #             (
    #                 pycom.Program(),
    #                 [1],
    #                 pycom.Program(
    #                     data={0: 1},
    #                     next_address=1,
    #                 ),
    #             ),
    #             (
    #                 pycom.Program(),
    #                 "a",
    #                 pycom.Program(
    #                     data={0: "a"},
    #                     next_address=2,
    #                 ),
    #             ),
    #             (
    #                 pycom.Program(),
    #                 [1, "a", 2],
    #                 pycom.Program(
    #                     data={
    #                         0: 1,
    #                         1: "a",
    #                         3: 2,
    #                     },
    #                     next_address=4,
    #                 ),
    #             ),
    #         ]
    #     ):
    #         with self.subTest(
    #             program=program,
    #             value=values,
    #             expected=expected,
    #         ):
    #             self.assertEqual(
    #                 program.with_values(*values),
    #                 expected,
    #             )

    # def test_with_label_at(self) -> None:
    #     self.assertEqual(
    #         pycom.Program().with_label_at(1, "a"),
    #         pycom.Program(labels={"a": 1}),
    #     )

    # def test_with_label(self) -> None:
    #     self.assertEqual(
    #         pycom.Program(next_address=1).with_label("a"),
    #         pycom.Program(
    #             next_address=1,
    #             labels={"a": 1},
    #         ),
    #     )

    # def test_label(self) -> None:
    #     self.assertEqual(
    #         pycom.Program(
    #             labels={"a": 1},
    #         ).label("a"),
    #         1,
    #     )

    # def test_label_not_found(self) -> None:
    #     with self.assertRaises(pycom.Program.LabelNotFoundError):
    #         pycom.Program().label("a")

    # def test_with_statement(self) -> None:
    #     self.assertEqual(
    #         pycom.Program(labels={"a": 1}).with_statement(
    #             self.TestStatement("a")
    #         ),
    #         pycom.Program(
    #             labels={"a": 1},
    #             next_address=1,
    #         ),
    #     )

    # def test_with_entry(self) -> None:
    #     for program, entry, expected in list[
    #         tuple[
    #             pycom.Program,
    #             pycom.Programs.program.Entry,
    #             pycom.Program,
    #         ]
    #     ](
    #         [
    #             (
    #                 pycom.Program(),
    #                 1,
    #                 pycom.Program(
    #                     data={0: 1},
    #                     next_address=1,
    #                 ),
    #             ),
    #             (
    #                 pycom.Program(
    #                     next_address=1,
    #                 ),
    #                 "a",
    #                 pycom.Program(
    #                     labels={"a": 1},
    #                     next_address=1,
    #                 ),
    #             ),
    #             (
    #                 pycom.Program(),
    #                 pycom.Instructions.NOP(),
    #                 pycom.Program(
    #                     data={
    #                         0: pycom.Instructions.NOP.value.operand_instance(
    #                             pycom.operands.None_,
    #                         ).opcode,
    #                     },
    #                     next_address=1,
    #                 ),
    #             ),
    #             (
    #                 pycom.Program(
    #                     labels={"a": 1},
    #                 ),
    #                 self.TestStatement("a"),
    #                 pycom.Program(
    #                     labels={"a": 1},
    #                     next_address=1,
    #                 ),
    #             ),
    #         ]
    #     ):
    #         with self.subTest(
    #             program=program,
    #             entry=entry,
    #             expected=expected,
    #         ):
    #             self.assertEqual(
    #                 program.with_entry(entry),
    #                 expected,
    #             )

    # def test_finalize_data(self) -> None:
    #     for program, expected in list[
    #         tuple[
    #             pycom.Program,
    #             typing.Optional[typing.Mapping[int, int]],
    #         ]
    #     ](
    #         [
    #             (
    #                 pycom.Program(),
    #                 {},
    #             ),
    #             (
    #                 pycom.Program().with_value(1),
    #                 {
    #                     0: 1,
    #                 },
    #             ),
    #             (
    #                 pycom.Program().with_value("a"),
    #                 None,
    #             ),
    #             (
    #                 pycom.Program().with_value("a").at(0xBEEF).with_label("a"),
    #                 {
    #                     0: 0xBE,
    #                     1: 0xEF,
    #                 },
    #             ),
    #         ]
    #     ):
    #         with self.subTest(
    #             program=program,
    #             expected=expected,
    #         ):
    #             if expected is None:
    #                 with self.assertRaises(pycom.Program.Error):
    #                     program.finalize_data()
    #             else:
    #                 self.assertDictEqual(
    #                     program.finalize_data(),
    #                     expected,
    #                 )
