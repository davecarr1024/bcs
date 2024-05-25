import typing
from pycom import bus, byte, component, control, register


class ALU(component.Component):
    CARRY = 0b00000001

    def __init__(
        self,
        bus: bus.Bus,
        name: typing.Optional[str] = None,
    ) -> None:
        self.bus = bus
        self.__lhs = register.Register(self.bus, "lhs")
        self.__rhs = register.Register(self.bus, "rhs")
        self.__result = register.Register(self.bus, "result")
        self.__status = register.Register(self.bus, "status")
        self.__add = control.Control("add")
        super().__init__(
            name or "alu",
            children=[
                self.__lhs,
                self.__rhs,
                self.__result,
                self.__status,
            ],
            controls=[
                self.__add,
            ],
        )

    @property
    def lhs(self) -> int:
        return self.__lhs.value

    @lhs.setter
    def lhs(self, lhs: int) -> None:
        self.__lhs.value = lhs

    @property
    def rhs(self) -> int:
        return self.__rhs.value

    @rhs.setter
    def rhs(self, rhs: int) -> None:
        self.__rhs.value = rhs

    @property
    def result(self) -> int:
        return self.__result.value

    @result.setter
    def result(self, result: int) -> None:
        self.__result.value = result

    @property
    def add(self) -> bool:
        return self.__add.value

    @add.setter
    def add(self, add: bool) -> None:
        self.__add.value = add

    @property
    def status(self) -> int:
        return self.__status.value

    @status.setter
    def status(self, status: int) -> None:
        self.__status.value = status

    @property
    def carry(self) -> bool:
        return bool(self.status & self.CARRY)

    @carry.setter
    def carry(self, carry: bool) -> None:
        if carry:
            self.status |= self.CARRY
        else:
            self.status &= ~self.CARRY

    def _set_result_and_status(self, result: int) -> None:
        self.result = result
        self.carry = result >= byte.Byte.max() or result < 0

    @typing.override
    def update(self) -> None:
        super().update()
        if self.add:
            self._set_result_and_status(int(self.carry) + self.lhs + self.rhs)
