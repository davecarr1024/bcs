import typing
from . import nary_gate


class Nand(nary_gate.NaryGate):
    @typing.override
    def _get_output(self, states: frozenset[bool]) -> bool:
        return not all(states)
