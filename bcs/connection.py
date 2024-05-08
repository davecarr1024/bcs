import dataclasses
import typing
from . import conductor, object_


@dataclasses.dataclass
class Connection(
    conductor.Conductor,
    typing.Sized,
    typing.Iterable["connector_lib.Connector"],
):
    _connectors: typing.Sequence["connector_lib.Connector"] = dataclasses.field(
        default_factory=list,
        repr=False,
        compare=False,
        init=False,
    )

    def __str__(self) -> str:
        return f"[{self.id}-{','.join(map(str,self))}]"

    def __len__(self) -> int:
        return len(self.connectors)

    def __iter__(self) -> typing.Iterator["connector_lib.Connector"]:
        return iter(self.connectors)

    @typing.override
    def _on_state_change(self, state: bool) -> None:
        for connector in self:
            connector.state = state

    @property
    def connectors(self) -> typing.Sequence["connector_lib.Connector"]:
        return self._connectors

    @connectors.setter
    def connectors(
        self, connectors: typing.Sequence["connector_lib.Connector"]
    ) -> None:
        self._connected_objects = self._connectors = connectors

    @typing.override
    def validate(self) -> None:
        for connector in self:
            if self not in connector:
                raise self.ValidationError(
                    f"connection {self} not in connector {connector}"
                )
        super().validate()

    @property
    def changing(self) -> bool:
        return any(connector.state != self.state for connector in self.connectors)

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        super().tick(t, dt)

    @typing.override
    def connect(self, rhs: conductor.Conductor) -> None:
        match rhs:
            case Connection():
                with self._pause_validation():
                    connector = connector_lib.Connector(
                        name="a",
                        component=component.Component(_name="buffer"),
                    )
                    self.connect(connector)
                    rhs.connect(connector)
            case connector_lib.Connector():
                if rhs not in self.connectors:
                    with self._pause_validation():
                        self.connectors = list(self.connectors) + [rhs]
                        rhs.connect(self)


from . import connector as connector_lib
from .components import component
