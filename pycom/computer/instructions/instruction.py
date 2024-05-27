import dataclasses
import typing
from pycom import controller
from pycom.computer.instructions import step as step_lib


@dataclasses.dataclass(frozen=True, kw_only=True)
class Instruction:
    @dataclasses.dataclass(frozen=True)
    class _StepsKey:
        status_mask: int
        status_value: int

    opcode: int
    _steps: dict[_StepsKey, list[step_lib.Step]] = dataclasses.field(
        default_factory=dict
    )

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
        status_mask: int,
        status_value: int,
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
                    status_mask=status_mask,
                    status_value=status_value,
                )
                for i, step in enumerate(steps[:-1])
            }
            | {
                steps[-1]
                .with_controls(last_control)
                .entry(
                    instruction=instruction,
                    instruction_counter=starting_instruction_counter + len(steps) - 1,
                    status_mask=status_mask,
                    status_value=status_value,
                )
            }
        )

    @classmethod
    def _preamble(cls) -> frozenset[controller.Controller.Entry]:
        return cls._entries_for_steps(
            instruction=None,
            starting_instruction_counter=0,
            reset_instruction_counter=False,
            status_mask=0,
            status_value=0,
            steps=cls.load_from_pc("controller.instruction_buffer.in"),
        )

    def entries(
        self,
    ) -> frozenset[controller.Controller.Entry]:
        preamble = self._preamble()
        entries: typing.MutableSet[controller.Controller.Entry] = set(preamble)
        for key, steps in self._steps.items():
            entries |= self._entries_for_steps(
                instruction=self.opcode,
                starting_instruction_counter=len(preamble),
                reset_instruction_counter=True,
                status_mask=key.status_mask,
                status_value=key.status_value,
                steps=steps,
            )
        return frozenset(entries)

    def _with_steps(self, steps: dict[_StepsKey, list[step_lib.Step]]) -> "Instruction":
        return Instruction(
            opcode=self.opcode,
            _steps=self._steps | steps,
        )

    def with_steps_for_status(
        self, status_mask: int, status_value: int, *steps: step_lib.Step
    ) -> "Instruction":
        return self._with_steps(
            {self._StepsKey(status_mask, status_value): list(steps)}
        )

    @classmethod
    def build(
        cls,
        opcode: int,
        *steps: step_lib.Step,
    ) -> "Instruction":
        return Instruction(
            opcode=opcode,
        ).with_steps_for_status(0, 0, *steps)
