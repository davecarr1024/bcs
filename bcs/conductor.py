import abc
import dataclasses
import random
import typing
from . import object_

MIN_STABLE_TIME: float = 0.5
PROPAGATION_MU: float = 0.01
PROPAGATION_SIGMA: float = 0.001


# Abstract conductor with state, connections, and propagation delay.
@dataclasses.dataclass
class Conductor(object_.Object):
    # The current state of the conductor.
    _state: bool = dataclasses.field(
        init=False,
        default=False,
        compare=False,
        repr=False,
    )
    # The last t seen.
    _t: float = dataclasses.field(
        default=0,
        init=False,
        compare=False,
        repr=False,
    )
    # The last time when state changed.
    _last_change_t: float = dataclasses.field(
        default=0,
        init=False,
        compare=False,
        repr=False,
    )
    # The minimum timespan between changes for this to be considered stable.
    _min_stable_time: float = dataclasses.field(
        default=MIN_STABLE_TIME,
        init=False,
        compare=False,
        repr=False,
    )
    # The mean of propagation times.
    _propagation_mu: float = dataclasses.field(
        default=PROPAGATION_MU,
        kw_only=True,
        compare=False,
        repr=False,
    )
    # The standard deviation of propagation timese.
    _propagation_sigma: float = dataclasses.field(
        default=PROPAGATION_SIGMA,
        kw_only=True,
        compare=False,
        repr=False,
    )
    # Is there a propagation happening.
    _propagation_active: bool = dataclasses.field(
        init=False,
        default=False,
        compare=False,
        repr=False,
    )
    # The timeout of the current propagation.
    _propagation_max_time: float = dataclasses.field(
        init=False,
        compare=False,
        repr=False,
    )
    # The time when the current propagation started.
    _propagation_start_time: float = dataclasses.field(
        init=False,
        compare=False,
        repr=False,
    )
    # The state that is propagating.
    _propagation_state: bool = dataclasses.field(
        init=False,
        compare=False,
        repr=False,
    )

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        self._t = t
        if (
            self._propagation_active
            and self._t - self._propagation_start_time >= self._propagation_max_time
        ):
            self._state = self._propagation_state
            self._propagation_active = False
            self._last_change_t = self._t
            self._on_state_change(self._state)

    @property
    def state(self) -> bool:
        return self._state

    @state.setter
    def state(self, state: bool) -> None:
        if (not self._propagation_active and state != self._state) or (
            self._propagation_active and state != self._propagation_state
        ):
            self._propagation_active = True
            self._propagation_max_time = random.gauss(
                self._propagation_mu, self._propagation_sigma
            )
            self._propagation_state = state
            self._propagation_start_time = self._t
            self._last_change_t = self._t

    @property
    def stable_time(self) -> float:
        return self._t - self._last_change_t

    @property
    @typing.override
    def is_stable(self) -> bool:
        return self.stable_time >= self._min_stable_time

    def is_stable_with_state(self, state: bool) -> bool:
        return self.is_stable and self.state == state

    def _on_state_change(self, state: bool) -> None: ...

    def run_until_stable_with_state(
        self,
        state: bool,
        *,
        max_t: float = object_.MAX_T,
        dt: float = object_.DT,
    ) -> float:
        def stable_with_state():
            return self.is_stable_with_state(state)

        try:
            return self.run_until(stable_with_state, max_t=max_t, dt=dt)
        except self.RunTimeout as e:
            raise self.RunTimeout(
                f"{self} failed to stabilze at state {state} in {max_t}s"
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
