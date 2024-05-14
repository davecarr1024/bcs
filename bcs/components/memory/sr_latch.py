from .. import component, logic


class SRLatch(component.Component):
    def __init__(
        self,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name=name, parent=parent)

        self.s_inverse = self.add_pin("s_inverse")
        self.r_inverse = self.add_pin("r_inverse")
        self.q = self.add_pin("q")
        self.q_inverse = self.add_pin("q_inverse")
        s_nand = logic.Nand(
            "s_nand",
            self,
            self.s_inverse,
            self.q_inverse,
        )
        s_nand.output.connect(self.q)
        r_nand = logic.Nand(
            "r_nand",
            self,
            self.r_inverse,
            self.q,
        )
        r_nand.output.connect(self.q_inverse)
