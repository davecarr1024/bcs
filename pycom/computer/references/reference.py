import abc


class Reference(abc.ABC):
    @abc.abstractmethod
    def __call__(
        self,
        output: "program.Program.Output",
        address: int,
    ) -> "program.Program.Output": ...

    @abc.abstractmethod
    def __len__(self) -> int: ...


from pycom.computer.programs import program
