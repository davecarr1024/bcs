import typing
from . import byte


class Bus:
    @typing.overload
    def __init__(self) -> None:
        ...

    @typing.overload
    def __init__(self, value: byte.Byte) -> None:
        ...

    def __init__(self, value: typing.Optional[byte.Byte] = None) -> None:
        self.value = value or byte.Byte()

    def __str__(self) -> str:
        return f"Bus({self.value})"

    @property
    def value(self) -> byte.Byte:
        return self._value

    @value.setter
    def value(self, value: byte.Byte) -> None:
        self._value = value
