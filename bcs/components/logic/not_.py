import dataclasses
import typing
from .. import component


@dataclasses.dataclass(kw_only=True)
class Not(component.Component):
    def __post_init__(self) -> None:
        self._a = self.add_connector("a")
        self._o = self.add_connector("o")

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        super().tick(t, dt)
        print(f"tick not {self._a.state} {self._o.state}")
        self._o.state = not self._a.state
