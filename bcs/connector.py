import dataclasses
import typing

from . import conductor, object_


@dataclasses.dataclass
class Connector(
    conductor.Conductor,
    typing.Sized,
    typing.Iterable["connection_lib.Connection"],
):
    name: str
    component: "component_lib.Component" = dataclasses.field(
        repr=False,
        compare=False,
    )
    _connections: typing.Sequence["connection_lib.Connection"] = dataclasses.field(
        default_factory=list,
        repr=False,
        compare=False,
        init=False,
    )

    def __str__(self) -> str:
        return f"{self.component}.{self.name}"

    def __post_init__(self):
        with self.component._pause_validation():
            with self._pause_validation():
                super().__post_init__()
                self.component.connectors = list(self.component.connectors) + [self]
                self.__update_connected_objects()

    def __update_connected_objects(self) -> None:
        self._connected_objects = [self.component] + list(self.connections)

    def __len__(self) -> int:
        return len(self.connections)

    def __iter__(self) -> typing.Iterator["connection_lib.Connection"]:
        return iter(self.connections)

    @property
    def connections(self) -> typing.Sequence["connection_lib.Connection"]:
        return self._connections

    @connections.setter
    def connections(
        self, connections: typing.Sequence["connection_lib.Connection"]
    ) -> None:
        with self._pause_validation():
            self._connections = connections
            self.__update_connected_objects()

    @typing.override
    def validate(self) -> None:
        if self not in self.component.connectors:
            raise self.ValidationError(
                f"connector {self} not in component {self.component}"
            )
        for connection in self:
            if self not in connection:
                raise self.ValidationError(
                    f"connector {self} not in connection {connection}"
                )
        super().validate()

    @typing.override
    def _on_state_change(self, state: bool) -> None:
        for connection in self:
            connection.state = state

    @typing.override
    def connect(self, rhs: conductor.Conductor) -> None:
        match rhs:
            case connection_lib.Connection():
                if rhs not in self.connections:
                    with self._pause_validation():
                        self.connections = list(self.connections) + [rhs]
                        rhs.connect(self)
            case Connector():
                with self._pause_validation():
                    connection = connection_lib.Connection()
                    self.connect(connection)
                    connection.connect(rhs)

    def connect_component(
        self, rhs: "component_lib.Component", rhs_connector_name: str
    ) -> None:
        self.connect(rhs[rhs_connector_name])


from . import connection as connection_lib
from .components import component as component_lib
