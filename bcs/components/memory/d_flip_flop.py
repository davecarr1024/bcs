from .. import component, logic, clock


class DFlipFlop(component.Component):
    def __init__(
        self,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name, parent)

        self.d = self.add_pin("d")
        self.enable = self.add_pin("enable")
        self.clk = self.add_pin("clk")
        self.q = self.add_pin("q")
        self.q_inverse = self.add_pin("q_inverse")

        s = self.d
        r = logic.Not(self.d, "d_not", self).output
        clk_edge = clock.EdgeDetector(self.clk, "clk_edge", self).output
        write = logic.And("write_and", self, clk_edge, self.enable).output
        s_nand = logic.Nand(
            "s_nand",
            self,
            s,
            write,
        )
        r_nand = logic.Nand(
            "r_nand",
            self,
            r,
            write,
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
