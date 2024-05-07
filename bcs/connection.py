import dataclasses
import typing
from . import conductor, object_


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
    update_time_limit: float = 0.01
    _update_time_limit: float = dataclasses.field(init=False, repr=False)
    _update_time: float = dataclasses.field(init=False, repr=False, default=0)

    def __len__(self) -> int:
        return len(self.connectors)

    def __iter__(self) -> typing.Iterator["connector_lib.Connector"]:
        return iter(self.connectors)

    @typing.override
    def validate(self) -> None:
        super().validate()
        assert all(self in connector.connections for connector in self.connectors)

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

    def connect(self, rhs: "connector_lib.Connector"):
        if rhs not in self.connectors:
            self.connectors.append(rhs)
            rhs.connect(self)
            self.validate()
            rhs.validate()


from . import connector as connector_lib
