import typing
from .. import object_


class Component(object_.Object, typing.Mapping[str, "pin.Pin"]):
    class PinKeyError(KeyError): ...

    def __init__(
        self,
        name: str | None = None,
        parent: typing.Optional["Component"] = None,
    ) -> None:
        super().__init__()
        self.__pins: typing.Mapping[str, pin.Pin] = {}
        self._name = name
        self.__parent = parent
        self.__children: frozenset[Component] = frozenset()
        if self.__parent is not None:
            with self._pause_validation():
                with self.__parent._pause_validation():
                    self.__parent.__children |= frozenset({self})
                    self._connected_objects |= {self.__parent}
                    self.__parent._connected_objects |= frozenset({self})

    def __len__(self) -> int:
        return len(self.pins)

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.pins)

    def __getitem__(self, name: str) -> "pin.Pin":
        return self.pin(name)

    def __str__(self) -> str:
        return self.path

    def _repr(self, indent: int) -> str:
        return f"\n{'  '*indent}{self.path} {self.states}{''.join(child._repr(indent+1) for child in self.children)}"

    def __repr__(self) -> str:
        return self._repr(0)

    @property
    def parent(self) -> typing.Optional["Component"]:
        return self.__parent

    @property
    def children(self) -> frozenset["Component"]:
        return self.__children

    @classmethod
    def type(cls) -> str:
        return cls.__name__

    @property
    def name(self) -> str:
        return self._name or self.type()

    @property
    def path(self) -> str:
        if self.parent is not None:
            return f"{self.parent.path}.{self.name}"
        else:
            return self.name

    @typing.override
    def validate(self) -> None:
        for pin in self.values():
            if pin.component is not self:
                raise self.ValidationError(
                    f"pin {pin} not connected to component {self}"
                )
        if self.parent is not None and self not in self.parent.children:
            raise self.ValidationError(f"component {self} not in parent {self.parent}")
        for child in self.children:
            if self is not child.parent:
                raise self.ValidationError(
                    f"component {self} is not connected to child {child}"
                )
        super().validate()

    @property
    def _pins(self) -> typing.Mapping[str, "pin.Pin"]:
        return self.__pins

    @_pins.setter
    def _pins(self, _pins: typing.Mapping[str, "pin.Pin"]) -> None:
        with self._pause_validation():
            self._connected_objects -= frozenset(self.__pins.values())
            self.__pins = _pins
            self._connected_objects |= frozenset(self.__pins.values())

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
        if any(self[name].state != state for name, state in states.items()):
            for name, state in states.items():
                self[name].state = state
            self.update()

    def print_all_states(self, prefix: str = "", indent: int = 0) -> None:
        print(f"{indent*'  '}{prefix}{self} {self.states}")
        for child in self.children:
            child.print_all_states("", indent + 1)


from .. import pin
