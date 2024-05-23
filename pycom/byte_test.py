import typing
import unittest

import pycom


class ByteTest(unittest.TestCase):
    def test_bits_to_int(self) -> None:
        for bits, expected in list[tuple[typing.Sequence[bool], typing.Optional[int]]](
            [
                (
                    [],
                    None,
                ),
                (
                    [False, False, False, False, False, False, False, False],
                    0,
                ),
                (
                    [False, False, False, False, False, False, False, True],
                    1,
                ),
                (
                    [False, True, False, True, False, True, False, True],
                    85,
                ),
                (
                    [True, True, True, True, True, True, True, True],
                    255,
                ),
                (
                    [True, True, True, True, True, True, True, True, True],
                    None,
                ),
            ]
        ):
            with self.subTest(bits=bits, expected=expected):
                if expected is None:
                    with self.assertRaises(pycom.Byte.Error):
                        pycom.Byte.bits_to_int(bits)
                else:
                    self.assertEqual(expected, pycom.Byte.bits_to_int(bits))

    def test_int_to_bits(self) -> None:
        for value, expected in list[tuple[int, typing.Sequence[bool]]](
            [
                (
                    0,
                    [False, False, False, False, False, False, False, False],
                ),
                (
                    1,
                    [False, False, False, False, False, False, False, True],
                ),
                (
                    85,
                    [False, True, False, True, False, True, False, True],
                ),
                (
                    255,
                    [True, True, True, True, True, True, True, True],
                ),
            ]
        ):
            with self.subTest(value=value, expected=expected):
                self.assertListEqual(
                    list(expected),
                    list(pycom.Byte.int_to_bits(value)),
                )

    def test_eq(self) -> None:
        for lhs, rhs, expected in list[tuple[pycom.Byte, pycom.Byte | int, bool]](
            [
                (pycom.Byte(1), pycom.Byte(1), True),
                (pycom.Byte(1), pycom.Byte(2), False),
                (pycom.Byte(1), 1, True),
                (pycom.Byte(1), 2, False),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs == rhs, expected)

    def test_wrap(self) -> None:
        self.assertEqual(pycom.Byte(0), pycom.Byte(256))

    def test_default(self) -> None:
        self.assertEqual(pycom.Byte(0), pycom.Byte())

    def test_bytes_to_int(self) -> None:
        self.assertEqual(
            pycom.Byte.bytes_to_int(
                pycom.Byte(0xBE),
                pycom.Byte(0xEF),
            ),
            0xBEEF,
        )

    def test_int_to_bytes(self) -> None:
        self.assertListEqual(
            list(pycom.Byte.int_to_bytes(0xBEEF)),
            [
                pycom.Byte(0xBE),
                pycom.Byte(0xEF),
            ],
        )

    def test_int_to_bytes_pad(self) -> None:
        self.assertListEqual(
            list(pycom.Byte.int_to_bytes(1)),
            [
                pycom.Byte(0),
                pycom.Byte(1),
            ],
        )

    def test_int_to_bytes_zero(self) -> None:
        self.assertListEqual(
            list(pycom.Byte.int_to_bytes(0)),
            [
                pycom.Byte(0),
                pycom.Byte(0),
            ],
        )

    def test_result_with_carry_for_value(self) -> None:
        for value, expected in list[tuple[int, pycom.Byte.ResultWithCarry]](
            [
                (
                    0,
                    pycom.Byte.ResultWithCarry(
                        pycom.Byte(0),
                        False,
                    ),
                ),
                (
                    1,
                    pycom.Byte.ResultWithCarry(
                        pycom.Byte(1),
                        False,
                    ),
                ),
                (
                    pycom.Byte.max(),
                    pycom.Byte.ResultWithCarry(
                        pycom.Byte(0),
                        True,
                    ),
                ),
                (
                    pycom.Byte.max() + 1,
                    pycom.Byte.ResultWithCarry(
                        pycom.Byte(1),
                        True,
                    ),
                ),
            ]
        ):
            with self.subTest(value=value, expected=expected):
                self.assertEqual(
                    pycom.Byte.ResultWithCarry.for_value(value),
                    expected,
                )

    def test_add(self) -> None:
        for lhs, rhs, expected in list[
            tuple[
                pycom.Byte,
                pycom.Byte | pycom.Byte.ResultWithCarry,
                pycom.Byte.ResultWithCarry,
            ]
        ](
            [
                (
                    pycom.Byte(1),
                    pycom.Byte(2),
                    pycom.Byte.ResultWithCarry(pycom.Byte(3), False),
                ),
                (
                    pycom.Byte(1),
                    pycom.Byte(pycom.Byte.max() - 1),
                    pycom.Byte.ResultWithCarry(pycom.Byte(0), True),
                ),
                (
                    pycom.Byte(1),
                    pycom.Byte.ResultWithCarry(pycom.Byte(2), False),
                    pycom.Byte.ResultWithCarry(pycom.Byte(3), False),
                ),
                (
                    pycom.Byte(1),
                    pycom.Byte.ResultWithCarry(pycom.Byte(2), True),
                    pycom.Byte.ResultWithCarry(pycom.Byte(4), False),
                ),
                (
                    pycom.Byte(1),
                    pycom.Byte.ResultWithCarry(pycom.Byte(pycom.Byte.max() - 2), True),
                    pycom.Byte.ResultWithCarry(pycom.Byte(0), True),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs + rhs, expected)

    def test_radd(self) -> None:
        for lhs, rhs, expected in list[
            tuple[pycom.Byte.ResultWithCarry, pycom.Byte, pycom.Byte.ResultWithCarry]
        ](
            [
                (
                    pycom.Byte.ResultWithCarry(pycom.Byte(1), False),
                    pycom.Byte(2),
                    pycom.Byte.ResultWithCarry(pycom.Byte(3), False),
                ),
                (
                    pycom.Byte.ResultWithCarry(pycom.Byte(1), True),
                    pycom.Byte(2),
                    pycom.Byte.ResultWithCarry(pycom.Byte(4), False),
                ),
                (
                    pycom.Byte.ResultWithCarry(pycom.Byte(1), True),
                    pycom.Byte(pycom.Byte.max() - 2),
                    pycom.Byte.ResultWithCarry(pycom.Byte(0), True),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(lhs + rhs, expected)

    def test_increment(self) -> None:
        for lhs, expected in list[tuple[pycom.Byte, pycom.Byte.ResultWithCarry]](
            [
                (
                    pycom.Byte(0),
                    pycom.Byte.ResultWithCarry(pycom.Byte(1), False),
                ),
                (
                    pycom.Byte(1),
                    pycom.Byte.ResultWithCarry(pycom.Byte(2), False),
                ),
                (
                    pycom.Byte(pycom.Byte.max() - 1),
                    pycom.Byte.ResultWithCarry(pycom.Byte(0), True),
                ),
            ]
        ):
            with self.subTest(lhs=lhs, expected=expected):
                self.assertEqual(lhs.increment(), expected)
