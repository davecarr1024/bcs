import abc
import dataclasses
import typing
from . import object_


@dataclasses.dataclass(kw_only=True)
class Conductor(object_.Object):
    _t: float = dataclasses.field(
        default=0,
        init=False,
    )
    _last_change_t: float = dataclasses.field(
        default=0,
        init=False,
    )
    _state: bool = False
    _min_stable_time: float = dataclasses.field(
        default=0.5,
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
            self._on_state_change(self._state)

    @property
    def stable_time(self) -> float:
        return self._t - self._last_change_t

    @property
    @typing.override
    def is_stable(self) -> bool:
        return self.stable_time >= self._min_stable_time

    def is_stable_with_state(self, state: bool) -> bool:
        return self.is_stable and self.state == state

    @abc.abstractmethod
    def _on_state_change(self, state: bool) -> None: ...

    def run_until_stable_with_state(
        self,
        state: bool,
        *,
        max_t: float = 10,
        dt: float = 0.01,
    ) -> float:
        def stable_with_state():
            return self.is_stable_with_state(state)

        try:
            return self.run_until(stable_with_state, max_t=max_t, dt=dt)
        except self.RunTimeout as e:
            raise self.RunTimeout(
                f"{self} failed to stabilze at state {state} in {max_t}s: {e}"
            )

    @abc.abstractmethod
    def connect(self, rhs: "Conductor") -> None: ...

    def connect_power(self) -> None:
        self.connect(components.Power()["o"])

    def connect_ground(self) -> None:
        self.connect(components.Ground()["o"])

    def not_(self) -> "Conductor":
        not_ = components.logic.Not()
        not_["a"].connect(self)
        return not_["o"]

    def __invert__(self) -> "Conductor":
        return self.not_()

    def and_(self, rhs: "Conductor") -> "Conductor":
        and_ = components.logic.And()
        and_["a"].connect(self)
        and_["b"].connect(rhs)
        return and_["o"]

    def __and__(self, rhs: "Conductor") -> "Conductor":
        return self.and_(rhs)

    def or_(self, rhs: "Conductor") -> "Conductor":
        or_ = components.logic.Or()
        or_["a"].connect(self)
        or_["b"].connect(rhs)
        return or_["o"]

    def __or__(self, rhs: "Conductor") -> "Conductor":
        return self.or_(rhs)

    def xor_(self, rhs: "Conductor") -> "Conductor":
        xor_ = components.logic.Xor()
        xor_["a"].connect(self)
        xor_["b"].connect(rhs)
        return xor_["o"]

    def __xor__(self, rhs: "Conductor") -> "Conductor":
        return self.xor_(rhs)


from . import connection, connector, components
