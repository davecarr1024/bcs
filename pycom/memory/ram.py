import typing
from pycom import byte
from pycom.memory import rom


class RAM(rom.ROM, typing.MutableMapping[int, byte.Byte]):
    @typing.override
    def __setitem__(self, address: int, value: byte.Byte) -> None:
        self._validate_address(address)
        self._data[address] = value

    @typing.override
    def __delitem__(self, address: int) -> None:
        self._validate_address(address)
        del self._data[address]
