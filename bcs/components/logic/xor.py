import typing
from . import nary_gate


class Xor(nary_gate.NaryGate):
    @typing.override
    def _get_output(self, states: frozenset[bool]) -> bool:
        return any(states) and not all(states)
