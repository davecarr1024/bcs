import typing
from .. import component
from ... import pin


class EdgeDetector(component.Component):
    def __init__(
        self,
        input: pin.Pin,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name=name, parent=parent)
        self.input = self.add_pin("input")
        self.input.connect(input)
        self.output = self.add_pin("output")
        self._last_state = self.input.state

    @typing.override
    def update(self) -> None:
        super().update()
        self.output.state = self.input.state and not self._last_state
        self._last_state = self.input.state
