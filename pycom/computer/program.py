import dataclasses
import typing


@dataclasses.dataclass(frozen=True)
class Program:
    data: dict[int, int] = dataclasses.field(default_factory=dict)

    def as_computer(self) -> "computer.Computer":
        return computer.Computer(data=self.data)

    @property
    def _next_address(self) -> int:
        return max([-1] + list(self.data.keys())) + 1

    def with_data(self, data: dict[int, int]) -> "Program":
        return Program(self.data | data)

    def with_value_at(
        self,
        address: int,
        value: int,
    ) -> "Program":
        return self.with_data({address: value})

    def with_value(self, value: int) -> "Program":
        return self.with_value_at(self._next_address, value)

    def with_values_at(self, address: int, *values: int) -> "Program":
        return self.with_data({address + i: value for i, value in enumerate(values)})

    def with_values(
        self,
        *values: int,
    ) -> "Program":
        return self.with_values_at(self._next_address, *values)


from . import computer
