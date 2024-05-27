import dataclasses
import typing
from pycom import controller
from pycom.computer.instructions import step as step_lib


@dataclasses.dataclass(frozen=True, kw_only=True)
class Instruction:
    opcode: int
    _steps: list[step_lib.Step] = dataclasses.field(default_factory=list)

    @classmethod
    def step(cls, *controls: str) -> step_lib.Step:
        return step_lib.Step().with_controls(*controls)

    @classmethod
    def steps(cls, *steps: step_lib.Step) -> list[step_lib.Step]:
        return list(steps)

    @classmethod
    def load_from_pc(cls, dest: str) -> list[step_lib.Step]:
        return cls.steps(
            cls.step(
                "program_counter.high_byte.out",
                "memory.address_high_byte.in",
            ),
            cls.step(
                "program_counter.low_byte.out",
                "memory.address_low_byte.in",
            ),
            cls.step(
                "memory.out",
                "program_counter.increment",
                dest,
            ),
        )

    @classmethod
    def load_addr_at_pc(cls) -> list[step_lib.Step]:
        return cls.steps(
            *cls.load_from_pc("controller.address_buffer.in"),
            *cls.load_from_pc("memory.address_low_byte.in"),
            cls.step(
                "controller.address_buffer.out",
                "memory.address_high_byte.in",
            ),
        )

    @classmethod
    def load_from_addr_at_pc(cls, dest: str) -> list[step_lib.Step]:
        return cls.steps(
            *cls.load_addr_at_pc(),
            cls.step(
                "memory.out",
                dest,
            ),
        )

    @classmethod
    def store_to_addr_at_pc(cls, src: str) -> list[step_lib.Step]:
        return cls.steps(
            *cls.load_addr_at_pc(),
            cls.step(
                src,
                "memory.in",
            ),
        )

    @classmethod
    def _entries_for_steps(
        cls,
        *,
        instruction: typing.Optional[int],
        starting_instruction_counter: int,
        reset_instruction_counter: bool,
        steps: list[step_lib.Step],
    ) -> frozenset[controller.Controller.Entry]:
        reset_control = "controller.instruction_counter.reset"
        increment_control = "controller.instruction_counter.increment"
        last_control = reset_control if reset_instruction_counter else increment_control
        steps = steps or [step_lib.Step()]
        return frozenset(
            {
                step.with_controls(increment_control).entry(
                    instruction=instruction,
                    instruction_counter=starting_instruction_counter + i,
                )
                for i, step in enumerate(steps[:-1])
            }
            | {
                steps[-1]
                .with_controls(last_control)
                .entry(
                    instruction=instruction,
                    instruction_counter=starting_instruction_counter + len(steps) - 1,
                )
            }
        )

    @classmethod
    def _preamble(cls) -> frozenset[controller.Controller.Entry]:
        return cls._entries_for_steps(
            instruction=None,
            starting_instruction_counter=0,
            reset_instruction_counter=False,
            steps=cls.load_from_pc("controller.instruction_buffer.in"),
        )

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
        *steps: step_lib.Step,
    ) -> "Instruction":
        return Instruction(
            opcode=opcode,
            _steps=list(steps),
        )
