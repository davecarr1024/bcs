import typing
from . import nary_gate


class And(nary_gate.NaryGate):
    @typing.override
    def _get_output(self, states: frozenset[bool]) -> bool:
        return all(states)
