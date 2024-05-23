import typing

from pycom import validatable


class Signal(validatable.Validatable):
    def __init__(
        self,
        name: str,
        component: typing.Optional["component_lib.Component"] = None,
    ) -> None:
        super().__init__()
        self.__name = name
        self.__component = None
        self.__value = False
        if component is not None:
            self.component = component

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> str:
        return (
            f"{self.component.path}.{self.name}"
            if self.component is not None
            else self.name
        )

    @property
    def component(self) -> typing.Optional["component_lib.Component"]:
        return self.__component

    @component.setter
    def component(self, component: typing.Optional["component_lib.Component"]) -> None:
        if component is not self.__component:
            with self._pause_validation():
                if self.__component is not None:
                    self.__component.remove_signal(self)
                self.__component = component
                if self.__component is not None:
                    self.__component.add_signal(self)

    @property
    def value(self) -> bool:
        return self.__value

    @value.setter
    def value(self, value: bool) -> None:
        self.__value = value

    @typing.override
    def validate(self) -> None:
        if self.component is not None and self not in self.component.signals:
            raise self.ValidationError(
                f"signal {self} not in component {self.component}"
            )


from . import component as component_lib
