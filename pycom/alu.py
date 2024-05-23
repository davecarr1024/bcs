import typing
from pycom import bus, byte, component, control, flag, register


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

    @property
    def lhs(self) -> byte.Byte:
        return self.__lhs.value

    @lhs.setter
    def lhs(self, lhs: byte.Byte) -> None:
        self.__lhs.value = lhs

    @property
    def rhs(self) -> byte.Byte:
        return self.__rhs.value

    @rhs.setter
    def rhs(self, rhs: byte.Byte) -> None:
        self.__rhs.value = rhs

    @property
    def result(self) -> byte.Byte:
        return self.__result.value

    @result.setter
    def result(self, result: byte.Byte) -> None:
        self.__result.value = result

    @property
    def add(self) -> bool:
        return self.__add.value

    @add.setter
    def add(self, add: bool) -> None:
        self.__add.value = add

    @property
    def carry(self) -> bool:
        return self.__carry.value

    @carry.setter
    def carry(self, carry: bool) -> None:
        self.__carry.value = carry

    def update(self) -> None:
        super().update()
        if self.add:
            result_with_carry = byte.Byte(int(self.carry)) + self.lhs + self.rhs
            self.carry = result_with_carry.carry
            self.result = result_with_carry.result
