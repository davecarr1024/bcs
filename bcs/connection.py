import dataclasses
import typing
from . import conductor, object_

_id = 0


@dataclasses.dataclass(kw_only=True)
class Connection(
    conductor.Conductor,
    typing.Sized,
    typing.Iterable["connector_lib.Connector"],
):
    connectors: typing.MutableSequence["connector_lib.Connector"] = dataclasses.field(
        default_factory=list,
        repr=False,
    )
    update_time_limit: float = 0.1
    _update_time: float = 0
    _id: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        global _id
        self._id = _id
        _id += 1
        super().__post_init__()

    def __str__(self) -> str:
        return f"[{','.join(map(str,self))}]"

    def __len__(self) -> int:
        return len(self.connectors)

    def __iter__(self) -> typing.Iterator["connector_lib.Connector"]:
        return iter(self.connectors)

    @typing.override
    def validate(self) -> None:
        for connector in self:
            if self not in connector:
                raise self.ValidationError(
                    f"connection {self} not in connector {connector}"
                )
        super().validate()

    @typing.override
    def _on_state_change(self, state: bool) -> None:
        self._update_time = 0

    @property
    def changing(self) -> bool:
        return any(connector.state != self.state for connector in self.connectors)

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        super().tick(t, dt)
        if self.changing:
            self._update_time += dt
            if self._update_time >= self.update_time_limit:
                for connector in self.connectors:
                    connector.state = self._state

    @property
    @typing.override
    def connected_objects(self) -> typing.Iterable[object_.Object]:
        return self.connectors

    @typing.override
    def connect(self, rhs: conductor.Conductor) -> None:
        match rhs:
            case Connection():
                connector = connector_lib.Connector(
                    name="a",
                    component=component.Component(_name="buffer"),
                )
                self.connect(connector)
                rhs.connect(connector)
            case connector_lib.Connector():
                if rhs not in self.connectors:
                    self.connectors.append(rhs)
                    rhs.connect(self)
                    self.validate()
                    rhs.validate()


from . import connector as connector_lib
from .components import component
