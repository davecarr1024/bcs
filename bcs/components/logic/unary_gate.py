import abc
import typing
from .. import component
from ... import pin


class UnaryGate(component.Component, abc.ABC):
    def __init__(self, input: pin.Pin, name: str | None = None) -> None:
        super().__init__(name)
        self.input = self.add_pin("input")
        self.input.connect(input)
        self.output = self.add_pin("output")
        self.update()

    @abc.abstractmethod
    def _get_output(self, state: bool) -> bool: ...

    @typing.override
    def update(self) -> None:
        self.output.state = self._get_output(self.input.state)
