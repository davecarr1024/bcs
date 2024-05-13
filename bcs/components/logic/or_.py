import typing
from . import nary_gate


class Or(nary_gate.NaryGate):
    @typing.override
    def _get_output(self, states: frozenset[bool]) -> bool:
        return any(states)
