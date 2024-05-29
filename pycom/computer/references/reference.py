import abc


class Reference(abc.ABC):
    @abc.abstractmethod
    def __call__(
        self,
        output: "program.Program.Output",
        address: int,
    ) -> "program.Program.Output": ...

    @classmethod
    @abc.abstractmethod
    def size(cls) -> int: ...


from pycom.computer.programs import program
