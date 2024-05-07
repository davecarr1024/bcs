import dataclasses
import typing
from .. import object_


@dataclasses.dataclass(kw_only=True)
class Component(
    object_.Object,
    typing.Mapping[str, "connector_lib.Connector"],
):
    connectors: typing.MutableSequence["connector_lib.Connector"] = dataclasses.field(
        default_factory=list,
        repr=False,
    )
    _t: float = dataclasses.field(
        default=0,
        repr=False,
        compare=False,
        init=False,
    )

    def __len__(self) -> int:
        return len(self.connectors)

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.connectors_by_name.keys())

    def __getitem__(self, name: str) -> "connector_lib.Connector":
        return self.connectors_by_name[name]

    @property
    def connectors_by_name(self) -> typing.Mapping[str, "connector_lib.Connector"]:
        return {connector.name: connector for connector in self.connectors}

    def connector(self, name: str) -> "connector_lib.Connector":
        return self.connectors_by_name[name]

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @typing.override
    def validate(self) -> None:
        super().validate()
        assert len(self.connectors) == len(self.connectors_by_name)
        assert all(connector.component == self for connector in self.connectors)

    @property
    @typing.override
    def connected_objects(self) -> typing.Iterable[object_.Object]:
        return self.connectors

    @typing.override
    def tick(self, t: float, dt: float) -> None:
        self._t = t
        print(f"tick component {self} {t} {dt}")

    @property
    @typing.override
    def is_stable(self) -> bool:
        return all(connector.is_stable for connector in self.connectors)

    def add_connector(self, name: str) -> "connector_lib.Connector":
        connector = connector_lib.Connector(component=self, name=name)
        return connector


from .. import connector as connector_lib
