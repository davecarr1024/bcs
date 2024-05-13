import typing
from . import object_


class Component(object_.Object, typing.Mapping[str, "pin.Pin"]):
    class PinKeyError(KeyError): ...

    def __init__(self, name: str | None = None) -> None:
        super().__init__()
        self.__pins: typing.Mapping[str, pin.Pin] = {}
        self._name = name

    def __len__(self) -> int:
        return len(self.pins)

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.pins)

    def __getitem__(self, name: str) -> "pin.Pin":
        return self.pin(name)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def type(cls) -> str:
        return cls.__name__

    @property
    def name(self) -> str:
        return self._name or self.type()

    @typing.override
    def validate(self) -> None:
        for pin in self.values():
            if pin.component is not self:
                raise self.ValidationError(
                    f"pin {self} not connected to component {self}"
                )
        super().validate()

    @property
    def _pins(self) -> typing.Mapping[str, "pin.Pin"]:
        return self.__pins

    @_pins.setter
    def _pins(self, _pins: typing.Mapping[str, "pin.Pin"]) -> None:
        with self._pause_validation():
            self.__pins = _pins
            self._connected_objects = frozenset(_pins.values())

    @property
    def pins(self) -> typing.Mapping[str, "pin.Pin"]:
        return self._pins

    def pin(self, name: str) -> "pin.Pin":
        if name not in self.pins:
            raise self.PinKeyError(
                f"unknown pin {name} in component {self} with pins {list(self)}"
            )
        return self.pins[name]

    def add_pin(self, name: str) -> "pin.Pin":
        with self._pause_validation():
            return pin.Pin(name, self)

    @property
    def states(self) -> typing.Mapping[str, bool]:
        return {name: pin.state for name, pin in self.items()}

    @states.setter
    def states(self, states: typing.Mapping[str, bool]) -> None:
        for name, state in states.items():
            self[name].state = state

    def _on_pin_update(self) -> None: ...


from . import pin
