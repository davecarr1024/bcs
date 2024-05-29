import abc
from . import program


class Statement(abc.ABC):
    @abc.abstractmethod
    def __call__(self, program: program.Program) -> program.Program: ...
