from .. import component, logic, clock


class SRFlipFLop(component.Component):
    def __init__(
        self,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name, parent)

        self.s = self.add_pin("s")
        self.r = self.add_pin("r")
        self.clk = self.add_pin("clk")
        self.q = self.add_pin("q")
        self.q_inverse = self.add_pin("q_inverse")

        clk_edge = clock.EdgeDetector(self.clk, "clk_edge", self)
        s_nand = logic.Nand(
            "s_nand",
            self,
            self.s,
            clk_edge.output,
        )
        r_nand = logic.Nand(
            "r_nand",
            self,
            self.r,
            clk_edge.output,
        )
        q_nand = logic.Nand(
            "q_nand",
            self,
            s_nand.output,
            self.q_inverse,
        )
        q_inverse_nand = logic.Nand(
            "q_inverse_nand",
            self,
            r_nand.output,
            self.q,
        )
        q_nand.output.connect(self.q)
        q_inverse_nand.output.connect(self.q_inverse)
