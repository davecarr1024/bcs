import dataclasses
import typing

from bcs.components import component


@dataclasses.dataclass
class EdgeDetector(component.Component):
    _last_state: bool = dataclasses.field(
        default=False,
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        self._a = self.add_connector("a")
        self._o = self.add_connector("o")

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        if not self._last_state and self._a.state:
            self._last_state = self._a.state
            self._o.state = True
        else:
            self._o.state = False
