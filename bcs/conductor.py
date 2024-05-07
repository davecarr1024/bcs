import abc
import dataclasses
import typing
from . import object_


@dataclasses.dataclass(kw_only=True)
class Conductor(object_.Object):
    _t: float = dataclasses.field(
        default=0,
        repr=False,
        compare=False,
        init=False,
    )
    _last_change_t: float = dataclasses.field(
        default=0,
        repr=False,
        compare=False,
        init=False,
    )
    _state: bool = False
    _min_stable_time: float = dataclasses.field(
        default=0.5,
        repr=False,
        compare=False,
        init=False,
    )

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        self._t = t

    @property
    def state(self) -> bool:
        return self._state

    @state.setter
    def state(self, state: bool) -> None:
        if state != self._state:
            self._state = state
            self._last_change_t = self._t
            print(f"{self} got state {self._state} at {self._t}")
            self._on_state_change(self._state)

    @property
    def stable_time(self) -> float:
        return self._t - self._last_change_t

    @property
    @typing.override
    def is_stable(self) -> bool:
        return self.stable_time >= self._min_stable_time

    @abc.abstractmethod
    def _on_state_change(self, state: bool) -> None: ...

    def run_until_state(
        self,
        state: bool,
        *,
        max_t: float = 10,
        dt: float = 0.01,
    ) -> float:
        t = self.run_until_stable(max_t=max_t, dt=dt)
        if self.state != state:
            raise Exception(f"{self} failed to stabilze at state {state}")
        return t
