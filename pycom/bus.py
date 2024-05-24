import typing
from . import byte


class Bus:
    def __init__(self, value: int = 0) -> None:
        self.__value = byte.Byte(value)

    def __str__(self) -> str:
        return f"Bus({self.value})"

    @property
    def value(self) -> int:
        return self.__value.value

    @value.setter
    def value(self, value: int) -> None:
        self.__value = byte.Byte(value)
