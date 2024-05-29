import typing
import unittest

from pycom.components import validatable


class ValidatableTest(unittest.TestCase):
    class TestObject(validatable.Validatable):
        def __init__(self) -> None:
            super().__init__()
            self.__valid = True

        @property
        def valid(self) -> bool:
            return self.__valid

        @valid.setter
        def valid(self, valid: bool) -> None:
            with self._pause_validation():
                self.__valid = valid

        @typing.override
        def validate(self) -> None:
            if not self.valid:
                raise self.ValidationError("invalid")

        def valid_operation(self) -> None:
            with self._pause_validation():
                self.valid = False
                self.valid = True

        def invalid_operation(self) -> None:
            self.valid = False
            self.valid = True

    def test_empty(self) -> None:
        self.TestObject()

    def test_valid_operation(self) -> None:
        self.TestObject().valid_operation()

    def test_invalid_operation(self) -> None:
        with self.assertRaises(self.TestObject.ValidationError):
            self.TestObject().invalid_operation()
