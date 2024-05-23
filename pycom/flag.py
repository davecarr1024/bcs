import typing
from pycom import component, control, signal


class Flag(component.Component):
    def __init__(self, name: str) -> None:
        self.__enable = control.Control(
            "enable",
            lambda _: self.__enable_or_disable(),
        )
        self.__disable = control.Control(
            "disable",
            lambda _: self.__enable_or_disable(),
        )
        self.__value = signal.Signal("value")
        super().__init__(
            name,
            controls=[self.__enable, self.__disable],
            signals=[self.__value],
        )

    @property
    def enable(self) -> bool:
        return self.__enable.value

    @enable.setter
    def enable(self, enable: bool) -> None:
        self.__set_enable_and_disable(True, False)

    @property
    def disable(self) -> bool:
        return self.__disable.value

    @disable.setter
    def disable(self, disable: bool) -> None:
        self.__set_enable_and_disable(False, True)

    def __set_enable_and_disable(self, enable: bool, disable: bool) -> None:
        self.__enable.value = False
        self.__disable.value = False
        self.__enable.value = enable
        self.__disable.value = disable

    def __enable_or_disable(self) -> None:
        if not control.Control.disjoint(self.__enable, self.__disable):
            raise self.Error(f"enable and disable set together")
        if self.enable:
            self.value = True
        elif self.disable:
            self.value = False

    @property
    def value(self) -> bool:
        return self.__value.value

    @value.setter
    def value(self, value: bool) -> None:
        if value != self.__value.value:
            self.__value.value = value
            self.__set_enable_and_disable(value, not value)

    @typing.override
    def update(self) -> None:
        self.__enable_or_disable()
        super().update()
