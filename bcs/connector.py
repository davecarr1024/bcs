import dataclasses
import typing

from .components import component as component_lib
from . import conductor, object_


@dataclasses.dataclass(kw_only=True)
class Connector(
    conductor.Conductor,
    typing.Sized,
    typing.Iterable["connection_lib.Connection"],
):
    name: str
    component: "component_lib.Component"
    connections: typing.MutableSequence[
        "connection_lib.Connection"
    ] = dataclasses.field(
        default_factory=list,
        repr=False,
    )

    def __post_init__(self):
        self.component.connectors.append(self)
        super().__post_init__()

    def __len__(self) -> int:
        return len(self.connections)

    def __iter__(self) -> typing.Iterator["connection_lib.Connection"]:
        return iter(self.connections)

    @typing.override
    def validate(self) -> None:
        super().validate()
        assert all(self in connection.connectors for connection in self.connections)
        assert self in self.component.connectors

    @typing.override
    def _on_state_change(self, state: bool) -> None:
        print(f"connector {self.name} got state {state}")
        for connection in self.connections:
            connection.state = state

    @property
    @typing.override
    def connected_objects(self) -> typing.Iterable[object_.Object]:
        return [self.component] + list(self.connections)

    @property
    def connected_components(self) -> typing.Iterable["component_lib.Component"]:
        components: typing.MutableSequence[component_lib.Component] = []
        for connection in self.connections:
            for connector in connection.connectors:
                component = connector.component
                if component not in components:
                    components.append(component)
        return components

    def connect(self, rhs: "connection_lib.Connection|Connector") -> None:
        match rhs:
            case connection_lib.Connection():
                if rhs not in self.connections:
                    self.connections.append(rhs)
                    rhs.connect(self)
                    self.validate()
                    rhs.validate()
            case Connector():
                connection = connection_lib.Connection()
                self.connect(connection)
                connection.connect(rhs)


from . import connection as connection_lib
