import abc
import typing
from .. import component
from ... import pin


class NaryGate(component.Component, abc.ABC):
    def __init__(
        self,
        name: str | None = None,
        parent: component.Component | None = None,
        *inputs: pin.Pin,
    ) -> None:
        super().__init__(name, parent)
        input_pins: set[pin.Pin] = set()
        for i, input in enumerate(inputs):
            input_pin = self.add_pin(f"input_{i}")
            input_pin.connect(input)
            input_pins.add(input_pin)
        self.inputs = frozenset(input_pins)
        self.output = self.add_pin("output")

    @abc.abstractmethod
    def _get_output(self, states: frozenset[bool]) -> bool:
        ...

    @typing.override
    def update(self) -> None:
        self.output.state = self._get_output(
            frozenset(input.state for input in self.inputs)
        )
