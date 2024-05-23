import typing
from pycom import bus, component, control, flag, register


class ALU(component.Component):
    def __init__(
        self,
        bus: bus.Bus,
        name: typing.Optional[str] = None,
    ) -> None:
        self.bus = bus
        self.__lhs = register.Register(self.bus, "lhs")
        self.__rhs = register.Register(self.bus, "rhs")
        self.__result = register.Register(self.bus, "result")
        self.__carry = flag.Flag("carry")
        self.__add = control.Control("add")
        super().__init__(
            name or "alu",
            children=[
                self.__lhs,
                self.__rhs,
                self.__result,
                self.__carry,
            ],
            controls=[
                self.__add,
            ],
        )
