import dataclasses
import typing
from pycom import controller


@dataclasses.dataclass(frozen=True, kw_only=True)
class Step:
    controls: frozenset[str] = dataclasses.field(default_factory=frozenset)
    status_mask: int = 0
    status_value: int = 0

    def with_controls(self, *controls: str) -> "Step":
        return Step(
            status_mask=self.status_mask,
            status_value=self.status_value,
            controls=self.controls | frozenset(controls),
        )

    def with_status(self, status_mask: int, status_value: bool) -> "Step":
        return Step(
            controls=self.controls,
            status_mask=self.status_mask | status_mask,
            status_value=(
                self.status_value | status_mask if status_value else self.status_value
            ),
        )

    def entry(
        self,
        *,
        instruction: typing.Optional[int] = None,
        instruction_counter: int,
    ) -> controller.Controller.Entry:
        return controller.Controller.Entry(
            instruction=instruction,
            instruction_counter=instruction_counter,
            status_mask=self.status_mask,
            status_value=self.status_value,
            controls=self.controls,
        )
