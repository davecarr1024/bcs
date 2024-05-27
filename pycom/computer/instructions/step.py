import dataclasses
import typing
from pycom import controller


@dataclasses.dataclass(frozen=True, kw_only=True)
class Step:
    controls: frozenset[str] = dataclasses.field(default_factory=frozenset)

    def with_controls(self, *controls: str) -> "Step":
        return Step(
            controls=self.controls | frozenset(controls),
        )

    def entry(
        self,
        *,
        instruction: typing.Optional[int] = None,
        instruction_counter: int,
        status_mask: int = 0,
        status_value: int = 0,
    ) -> controller.Controller.Entry:
        return controller.Controller.Entry(
            instruction=instruction,
            instruction_counter=instruction_counter,
            status_mask=status_mask,
            status_value=status_value,
            controls=self.controls,
        )
