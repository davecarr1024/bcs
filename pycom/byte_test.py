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
        for lhs, rhs, expected in list[tuple[int, int, bool]](
            [
                (1, 1, True),
                (1, 2, False),
            ]
        ):
            with self.subTest(lhs=lhs, rhs=rhs, expected=expected):
                self.assertEqual(expected, pycom.Byte(lhs) == pycom.Byte(rhs))

    def test_wrap(self) -> None:
        self.assertEqual(pycom.Byte(0), pycom.Byte(256))

    def test_default(self) -> None:
        self.assertEqual(pycom.Byte(0), pycom.Byte())
