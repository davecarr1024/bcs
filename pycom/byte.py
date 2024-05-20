import dataclasses
import typing


class Byte(typing.Sized, typing.Iterable[bool]):
    class Error(Exception): ...

    @dataclasses.dataclass(frozen=True)
    class ResultWithCarry:
        result: "Byte"
        carry: bool

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

    @typing.overload
    def __init__(self) -> None: ...

    @typing.overload
    def __init__(self, value: int) -> None: ...

    @typing.overload
    def __init__(self, value: typing.Sequence[bool]) -> None: ...

    def __init__(self, value: int | typing.Sequence[bool] = 0) -> None:
        if isinstance(value, typing.Sequence):
            value = self.bits_to_int(value)
        self.value = value

    def __eq__(self, rhs: object) -> bool:
        return isinstance(rhs, Byte) and self.value == rhs.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __len__(self) -> int:
        return self.size()

    def __iter__(self) -> typing.Iterator[bool]:
        return iter(self.bits)

    def __repr__(self) -> str:
        return f"{self._value:#0{4}x}"

    def __add__(self, rhs: "Byte") -> ResultWithCarry:
        carry = (value := self.value + rhs.value) >= self.max()
        return self.ResultWithCarry(Byte(value), carry)

    def increment(self) -> bool:
        result_and_carry = self + Byte(1)
        self.value = result_and_carry.result.value
        return result_and_carry.carry

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value % self.max()

    @property
    def bits(self) -> typing.Sequence[bool]:
        return self.int_to_bits(self._value)

    @bits.setter
    def bits(self, bits: typing.Sequence[bool]) -> None:
        self._value = self.bits_to_int(bits)
