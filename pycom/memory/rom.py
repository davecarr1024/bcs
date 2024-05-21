import collections
import dataclasses
import typing
from pycom import byte, component


class ROM(component.Component, typing.Mapping[int, byte.Byte]):
    class Error(Exception): ...

    @dataclasses.dataclass(frozen=True)
    class AddressError(Error, IndexError):
        address: int

    def __init__(
        self,
        name: str,
        size: int,
        data: typing.Optional[typing.Mapping[int, byte.Byte]] = None,
    ) -> None:
        super().__init__(name)
        self._size = size
        if data:
            for address in data.keys():
                self._validate_address(address)
        self.__data: typing.MutableMapping[int, byte.Byte] = collections.defaultdict(
            byte.Byte
        ) | dict(data or {})

    def _validate_address(self, address) -> None:
        if address < 0 or address >= self.size:
            raise self.AddressError(address)

    @property
    def size(self) -> int:
        return self._size

    @property
    def _data(self) -> typing.MutableMapping[int, byte.Byte]:
        return self.__data

    @_data.setter
    def _data(self, _data: typing.MutableMapping[int, byte.Byte]) -> None:
        self.__data = _data

    @property
    def data(self) -> typing.Mapping[int, byte.Byte]:
        return self._data

    @typing.override
    def __getitem__(self, address: int) -> byte.Byte:
        self._validate_address(address)
        return self.data[address]

    @typing.override
    def __len__(self) -> int:
        return len(self.data)

    @typing.override
    def __iter__(self) -> typing.Iterator[int]:
        return iter(self.data)
