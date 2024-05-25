import dataclasses
import typing
from pycom import controller
from pycom.computer import instruction, instruction_step


@dataclasses.dataclass(frozen=True, kw_only=True)
class SimpleInstruction(instruction.Instruction):
    opcode: int
    _steps: list[instruction_step.InstructionStep] = dataclasses.field(
        default_factory=list
    )

    @typing.override
    def entries(self) -> frozenset[controller.Controller.Entry]:
        preamble = self._preamble()
        return preamble | self._entries_for_steps(
            instruction=self.opcode,
            starting_instruction_counter=len(preamble),
            reset_instruction_counter=True,
            steps=self._steps,
        )

    @classmethod
    def build(
        cls,
        opcode: int,
        *steps: instruction_step.InstructionStep,
    ) -> "SimpleInstruction":
        return SimpleInstruction(
            opcode=opcode,
            _steps=list(steps),
        )
