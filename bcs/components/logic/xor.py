import dataclasses
import typing
from .. import component


@dataclasses.dataclass
class Xor(component.Component):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.a = self.add_connector("a")
        self.b = self.add_connector("b")
        self.o = self.add_connector("o")
        return super().__post_init__()

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        super().tick(t, dt)
        self.o.state = self.a.state ^ self.b.state
