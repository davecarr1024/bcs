import dataclasses
import typing
from . import component


@dataclasses.dataclass
class Clock(component.Component):
    period: float = 0.1
    _cycle_time: float = 0

    def __post_init__(self) -> None:
        super().__post_init__()
        self._en = self.add_connector("en")
        self._o = self.add_connector("o")

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        if self._en.state:
            self._cycle_time += dt
            while self._cycle_time > self.period:
                self._cycle_time -= self.period
                self._o.state = not self._o.state
