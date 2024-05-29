import typing
from pycom.components import validatable


class Control(validatable.Validatable):
    def __init__(
        self,
        name: str,
        on_change: typing.Optional[typing.Callable[[bool], None]] = None,
        *,
        component: typing.Optional["component_lib.Component"] = None,
    ) -> None:
        super().__init__()
        self.__name = name
        self.__value = False
        self.__on_change = on_change
        self.__pause_validation_count = 0
        self.__component = None
        if component is not None:
            self.component = component

    @typing.override
    def validate(self) -> None:
        if self.component is not None and self not in self.component.controls:
            raise self.ValidationError(
                f"control {self} not in component {self.component}"
            )

    @property
    def component(self) -> typing.Optional["component_lib.Component"]:
        return self.__component

    @component.setter
    def component(self, component: typing.Optional["component_lib.Component"]) -> None:
        if component is not self.__component:
            with self._pause_validation():
                if self.__component is not None:
                    self.__component.remove_control(self)
                self.__component = component
                if self.__component is not None:
                    self.__component.add_control(self)

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


from . import component as component_lib
