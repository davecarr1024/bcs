import typing


class Control:
    def __init__(
        self,
        name: str,
        on_change: typing.Optional[typing.Callable[[bool], None]] = None,
    ) -> None:
        self.__name = name
        self.__value = False
        self.__on_change = on_change

    @property
    def name(self) -> str:
        return self.__name

    @property
    def value(self) -> bool:
        return self.__value

    @value.setter
    def value(self, value: bool) -> None:
        self.__value = value
        if self.__on_change is not None:
            self.__on_change(self.__value)

    @staticmethod
    def disjoint(*controls: "Control") -> bool:
        return sum(control.value for control in controls) < 2
