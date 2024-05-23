import dataclasses
import typing


class Byte(typing.Sized, typing.Iterable[bool]):
    class Error(Exception): ...

    @dataclasses.dataclass(frozen=True)
    class ResultWithCarry:
        result: "Byte"
        carry: bool

        @property
        def value(self) -> int:
            return self.result.value + int(self.carry) * Byte.max()

        @staticmethod
        def for_value(value: int) -> "Byte.ResultWithCarry":
            return Byte.ResultWithCarry(Byte(value), value >= Byte.max())

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
    def bytes_to_int(cls, *bytes: "Byte") -> int:
        result = 0
        for i, byte in enumerate(reversed(bytes)):
            result |= byte.value << (i * cls.size())
        return result

    @classmethod
    def int_to_bytes(
        cls,
        value: int,
        min_num_bytes: int = 2,
    ) -> typing.Sequence["Byte"]:
        bytes: typing.MutableSequence[Byte] = []
        while value or len(bytes) < min_num_bytes:
            bytes.insert(0, Byte(value))
            value >>= cls.size()
        return bytes

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

    def __repr__(self) -> str:
        return f"{self._value:#0{4}x}"

    @typing.overload
    def __add__(self, rhs: "Byte") -> ResultWithCarry: ...

    @typing.overload
    def __add__(self, rhs: ResultWithCarry) -> ResultWithCarry: ...

    def __add__(self, rhs: typing.Union["Byte", ResultWithCarry]) -> ResultWithCarry:
        return self.ResultWithCarry.for_value(self.value + rhs.value)

    def __radd__(self, lhs: ResultWithCarry) -> ResultWithCarry:
        return self.ResultWithCarry.for_value(lhs.value + self.value)

    def increment(self) -> ResultWithCarry:
        return self + Byte(1)

    @property
    def value(self) -> int:
        return self._value

    @property
    def bits(self) -> typing.Sequence[bool]:
        return self.int_to_bits(self._value)
