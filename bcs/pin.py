import typing
from . import object_


class Pin(object_.Object, typing.Sized, typing.Iterable["Pin"]):
    def __init__(
        self,
        name: str,
        component: "component.Component",
    ) -> None:
        super().__init__()
        self.component = component
        self.name = name
        self.__connected_pins: frozenset[Pin] = frozenset()
        self.__all_connected_pins: frozenset[Pin] | None = frozenset({self})
        self.__state: bool = False
        if self.name in self.component:
            raise self.Error(
                f"pin {self.name} has duplicate name in component {self.component} with pins {list(self.component)}"
            )
        with self._pause_validation():
            self._connected_objects = frozenset((self.component,))
            self.component._pins = dict(self.component._pins) | {self.name: self}

    def __len__(self) -> int:
        return len(self.connected_pins)

    def __iter__(self) -> typing.Iterator["Pin"]:
        return iter(self.connected_pins)

    def __str__(self) -> str:
        return f"{self.component}.{self.name}"

    @typing.override
    def validate(self) -> None:
        if self.name not in self.component or self.component[self.name] is not self:
            raise self.ValidationError(f"pin {self} not in component {self.component}")
        for pin in self:
            if self not in pin:
                raise self.ValidationError(f"pin {self} not in connected pin {pin}")
        super().validate()

    @property
    def _connected_pins(self) -> frozenset["Pin"]:
        return self.__connected_pins

    @_connected_pins.setter
    def _connected_pins(self, _connected_pins: frozenset["Pin"]) -> None:
        with self._pause_validation():
            self._connected_objects -= self.__connected_pins
            self.__connected_pins = _connected_pins
            self._connected_objects |= self.__connected_pins

            if self.__all_connected_pins is not None:
                for pin in self.__all_connected_pins:
                    pin.__all_connected_pins = None

    @property
    def connected_pins(self) -> frozenset["Pin"]:
        return self._connected_pins

    @property
    def all_connected_pins(self) -> frozenset["Pin"]:
        if self.__all_connected_pins is None:
            traversed: set[Pin] = set()
            pending: set[Pin] = {self}
            while pending:
                pin = pending.pop()
                if pin not in traversed:
                    traversed.add(pin)
                    pending |= pin.connected_pins
            self.__all_connected_pins = frozenset(traversed)
        return self.__all_connected_pins

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        if state != self.__state:
            self.__state = state
            for pin in self:
                pin.state = state
            self.component.update()

    def connect(self, pin: "Pin") -> None:
        if pin not in self._connected_pins:
            with self._pause_validation():
                self._connected_pins |= {pin}
                pin.connect(self)

    def disconnect(self, pin: "Pin") -> None:
        if pin in self._connected_pins:
            with self._pause_validation():
                self._connected_pins -= {pin}
                pin.disconnect(self)

    def is_connected(self, pin: "Pin") -> bool:
        return pin in self.all_connected_pins

    def connect_power(self) -> None:
        self.disconnect(ground_.output)
        self.connect(power_.output)

    def connect_ground(self) -> None:
        self.disconnect(power_.output)
        self.connect(ground_.output)


from .components import component, power_, ground_
