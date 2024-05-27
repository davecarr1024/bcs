import abc


class Statement(abc.ABC):
    @abc.abstractmethod
    def __call__(self, program: "program.Program") -> "program.Program": ...


from . import program
