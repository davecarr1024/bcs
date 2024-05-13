import typing
from . import unary_gate


class Not(unary_gate.UnaryGate):
    @typing.override
    def _get_output(self, state: bool) -> bool:
        return not state
