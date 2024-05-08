import dataclasses
import typing
from .. import object_


@dataclasses.dataclass
class Component(
    object_.Object,
    typing.Mapping[str, "connector_lib.Connector"],
):
    class Error(Exception): ...

    _connectors: typing.Sequence["connector_lib.Connector"] = dataclasses.field(
        default_factory=list,
        repr=False,
        init=False,
        compare=False,
    )
    _t: float = dataclasses.field(
        default=0,
        init=False,
        compare=False,
        repr=False,
    )
    _name: typing.Optional[str] = None

    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        return len(self.connectors)

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.connectors_by_name.keys())

    def __getitem__(self, name: str) -> "connector_lib.Connector":
        return self.connector(name)

    @property
    def name(self) -> str:
        return self._name or self.type()

    @property
    def connectors(self) -> typing.Sequence["connector_lib.Connector"]:
        return self._connectors

    @connectors.setter
    def connectors(
        self, connectors: typing.Sequence["connector_lib.Connector"]
    ) -> None:
        self._connected_objects = self._connectors = connectors

    @property
    def connectors_by_name(self) -> typing.Mapping[str, "connector_lib.Connector"]:
        return {connector.name: connector for connector in self.connectors}

    def connector(self, name: str) -> "connector_lib.Connector":
        if name not in self.connectors_by_name:
            raise KeyError(
                f"trying to get unknown connector {name} from {self}: connectors are {list(self.keys())}"
            )
        return self.connectors_by_name[name]

    @classmethod
    def type(cls) -> str:
        return cls.__name__

    @typing.override
    def validate(self) -> None:
        if len(self.connectors) != len(self.connectors_by_name):
            raise self.ValidationError(
                f"{self} has duplicate connectors {self.connectors}"
            )
        for connector in self.values():
            if connector.component is not self:
                raise self.ValidationError(
                    f"component {self} not connected to connector {connector}"
                )
        super().validate()

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        self._t = t

    @property
    @typing.override
    def is_stable(self) -> bool:
        return all(connector.is_stable for connector in self.connectors)

    @property
    def state(self) -> typing.Mapping[str, bool]:
        return {name: connector.state for name, connector in self.items()}

    def is_stable_with_states(self, **states: bool) -> bool:
        return self.is_stable and self.has_states(**states)

    def has_states(self, **states: bool) -> bool:
        return all(self[name].state == state for name, state in states.items())

    def add_connector(self, name: str) -> "connector_lib.Connector":
        if name in self.keys():
            raise self.Error(f"{self} creating duplicate connector {name}")
        connector = connector_lib.Connector(component=self, name=name)
        return connector

    def run_until_stable_with_states(
        self,
        *,
        max_t: float = object_.MAX_T,
        dt: float = object_.DT,
        **state: bool,
    ) -> float:
        def stable_with_states() -> bool:
            return self.is_stable_with_states(**state)

        try:
            return self.run_until(stable_with_states, max_t=max_t, dt=dt)
        except self.RunTimeout:
            raise self.RunTimeout(
                f"{self} failed to stabilize at states {state} in {max_t}s - current state is {self.state}"
            )

    def run_until_states(
        self,
        *,
        max_t: float = object_.MAX_T,
        dt: float = object_.DT,
        **states: bool,
    ) -> float:
        def has_states() -> bool:
            return self.has_states(**states)

        try:
            return self.run_until(has_states, max_t=max_t, dt=dt)
        except self.RunTimeout:
            raise self.RunTimeout(
                f"{self} failed to stabilize at states {states} in {max_t}s - current state is {self.state}"
            )


from .. import connector as connector_lib
