import abc
import contextlib
import typing

from pycom.components import errorable


class Validatable(abc.ABC, errorable.Errorable):
    class ValidationError(errorable.Errorable.Error): ...

    def __init__(self) -> None:
        self.__pause_validation_count = 0

    @typing.final
    @property
    def _validation_enabled(self) -> bool:
        return self.__pause_validation_count == 0

    @typing.final
    @contextlib.contextmanager
    def _pause_validation(self) -> typing.Iterator[None]:
        try:
            self.__pause_validation_count += 1
            yield
        finally:
            self.__pause_validation_count -= 1
            self._validate_if_enabled()

    @typing.final
    def _validate_if_enabled(self) -> None:
        if self._validation_enabled:
            self.validate()

    @abc.abstractmethod
    def validate(self) -> None: ...
