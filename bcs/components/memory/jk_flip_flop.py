from .. import component, logic, clock


class JKFlipFlop(component.Component):
    def __init__(
        self,
        name: str | None = None,
        parent: component.Component | None = None,
    ) -> None:
        super().__init__(name=name, parent=parent)

        self.j = self.add_pin("j")
        self.k = self.add_pin("k")
        self.clk = self.add_pin("clk")
        self.q = self.add_pin("q")
        self.q_inverse = self.add_pin("q_inverse")

        clk_edge = clock.EdgeDetector("clk_edge", self)
        clk_edge.input.connect(self.clk)
        j_nand = logic.Nand(
            "j_nand",
            self,
            self.q_inverse,
            self.j,
            clk_edge.output,
        )
        k_nand = logic.Nand(
            "k_nand",
            self,
            self.q,
            self.k,
            clk_edge.output,
        )
        s_nand = logic.Nand(
            "s_nand",
            self,
            j_nand.output,
            self.q_inverse,
        )
        s_nand.output.connect(self.q)
        r_nand = logic.Nand(
            "r_nand",
            self,
            k_nand.output,
            self.q,
        )
        r_nand.output.connect(self.q_inverse)
