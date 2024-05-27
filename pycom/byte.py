import typing
from pycom import errorable


class Byte(
    errorable.Errorable,
    typing.Sized,
    typing.Iterable[bool],
):
    @classmethod
    def size(cls) -> int:
        return 8

    @classmethod
    def max(cls) -> int:
        return 1 << cls.size()

    @classmethod
    def bits_to_int(cls, bits: typing.Sequence[bool]) -> int:
        if len(bits) != cls.size():
            raise cls.Error(f"invalid num bits {len(bits)} != {cls.size()}")
        return sum(bit * (1 << (cls.size() - 1 - i)) for i, bit in enumerate(bits))

    @classmethod
    def int_to_bits(cls, value: int) -> typing.Sequence[bool]:
        return [bool(value & (1 << (cls.size() - 1 - i))) for i in range(cls.size())]

    @classmethod
    def partition(
        cls,
        value: int,
        min_num_parts: int = 2,
    ) -> typing.Sequence[int]:
        parts: typing.MutableSequence[int] = []
        while value or len(parts) < min_num_parts:
            parts.insert(0, value % cls.max())
            value >>= cls.size()
        return parts

    @classmethod
    def unpartition(cls, *parts: int) -> int:
        result = 0
        for i, part in enumerate(reversed(parts)):
            result |= part << (i * cls.size())
        return result

    @typing.overload
    def __init__(self) -> None: ...

    @typing.overload
    def __init__(self, value: int) -> None: ...

    @typing.overload
    def __init__(self, value: typing.Sequence[bool]) -> None: ...

    def __init__(self, value: int | typing.Sequence[bool] = 0) -> None:
        if isinstance(value, typing.Sequence):
            value = self.bits_to_int(value)
        self._value = value % self.max()

    def __eq__(self, rhs: object) -> bool:
        match rhs:
            case Byte():
                return self.value == rhs.value
            case int():
                return self.value == rhs
            case _:
                return False

    def __hash__(self) -> int:
        return hash(self.value)

    def __len__(self) -> int:
        return self.size()

    def __iter__(self) -> typing.Iterator[bool]:
        return iter(self.bits)

    @classmethod
    def hex_str(cls, value: int) -> str:
        return f"0x{value:X}"

    def __repr__(self) -> str:
        return self.hex_str(self._value)

    @property
    def value(self) -> int:
        return self._value

    @property
    def bits(self) -> typing.Sequence[bool]:
        return self.int_to_bits(self._value)
