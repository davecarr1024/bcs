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

    def test_partition(self) -> None:
        for value, expected in list[
            tuple[
                int,
                typing.Sequence[int],
            ]
        ](
            [
                (
                    0,
                    (0, 0),
                ),
                (
                    0x0001,
                    (0x00, 0x01),
                ),
                (
                    0xBEEF,
                    (0xBE, 0xEF),
                ),
                (
                    0xDEADBEEF,
                    (0xDE, 0xAD, 0xBE, 0xEF),
                ),
            ]
        ):
            with self.subTest(value=value, expected=expected):
                self.assertSequenceEqual(
                    pycom.Byte.partition(value),
                    expected,
                )

    def test_unpartition(self) -> None:
        for parts, expected in list[tuple[typing.Sequence[int], int]](
            [
                (
                    (0,),
                    0,
                ),
                (
                    (0x00, 0x01),
                    0x01,
                ),
                (
                    (0xBE, 0xEF),
                    0xBEEF,
                ),
                (
                    (0xDE, 0xAD, 0xBE, 0xEF),
                    0xDEADBEEF,
                ),
            ]
        ):
            with self.subTest(parts=parts, expected=expected):
                self.assertEqual(
                    pycom.Byte.unpartition(*parts),
                    expected,
                )
