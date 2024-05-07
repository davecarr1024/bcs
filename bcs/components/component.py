import dataclasses
import typing
from .. import object_


@dataclasses.dataclass(kw_only=True)
class Component(
    object_.Object,
    typing.Mapping[str, "connector_lib.Connector"],
):
    class Error(Exception): ...

    connectors: typing.MutableSequence["connector_lib.Connector"] = dataclasses.field(
        default_factory=list,
        repr=False,
    )
    _t: float = dataclasses.field(
        default=0,
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
        return self.connectors_by_name[name]

    @property
    def name(self) -> str:
        return self._name or self.type()

    @property
    def connectors_by_name(self) -> typing.Mapping[str, "connector_lib.Connector"]:
        return {connector.name: connector for connector in self.connectors}

    def connector(self, name: str) -> "connector_lib.Connector":
        if name not in self.connectors_by_name:
            raise self.Error(f'trying to get unknown connector {name} from {self}: connectors are {[','.join(self.keys())]}')
        return self.connectors_by_name[name]

    @classmethod
    def type(cls) -> str:
        return cls.__name__

    @typing.override
    def validate(self) -> None:
        duplicates = {connector.name for connector in self.connectors if self.connectors.count(connector.name) > 1}
        if duplicates:
            raise self.ValidationError(f'component {self} has duplicate connectors {duplicates}')
        for connector in self.values():
            if connector.component is not self:
                raise self.ValidationError(f'component {self} not connected to connector {connector}')
        super().validate()

    @property
    @typing.override
    def connected_objects(self) -> typing.Iterable[object_.Object]:
        return self.connectors

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        self._t = t

    @property
    @typing.override
    def is_stable(self) -> bool:
        return all(connector.is_stable for connector in self.connectors)

    def is_stable_with_state(self, **state: bool) -> bool:
        return all(
            self[name].is_stable_with_state(value) for name, value in state.items()
        )

    def add_connector(self, name: str) -> "connector_lib.Connector":
        if name in self.keys():
            raise self.Error(f'{self} creating duplicate connector {name}')
        connector = connector_lib.Connector(component=self, name=name)
        return connector

    def run_until_stable_with_state(
        self,
        *,
        max_t: float = 10,
        dt: float = 0.01,
        **state: bool,
    ) -> float:
        def stable_at_state() -> bool:
            return self.is_stable_with_state(**state)

        try:
            return self.run_until(stable_at_state, max_t=max_t, dt=dt)
        except self.RunTimeout:
            raise self.RunTimeout(
                f"{self} failed to stabilize at state {state} in {max_t}s"
            )


from .. import connector as connector_lib
