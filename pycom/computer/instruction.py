import abc
import typing
from pycom import controller
from pycom.computer import instruction_step


class Instruction(abc.ABC):
    @abc.abstractmethod
    def entries(self) -> frozenset[controller.Controller.Entry]: ...

    @classmethod
    def step(cls, *controls: str) -> instruction_step.InstructionStep:
        return instruction_step.InstructionStep().with_controls(*controls)

    @classmethod
    def steps(
        cls, *steps: instruction_step.InstructionStep
    ) -> list[instruction_step.InstructionStep]:
        return list(steps)

    @classmethod
    def load_from_pc(cls, dest: str) -> list[instruction_step.InstructionStep]:
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
    def load_addr_at_pc(cls) -> list[instruction_step.InstructionStep]:
        return cls.steps(
            *cls.load_from_pc("controller.address_buffer.in"),
            *cls.load_from_pc("memory.address_low_byte.in"),
            cls.step(
                "controller.address_buffer.out",
                "memory.address_high_byte.in",
            ),
        )

    @classmethod
    def load_from_addr_at_pc(cls, dest: str) -> list[instruction_step.InstructionStep]:
        return cls.steps(
            *cls.load_addr_at_pc(),
            cls.step(
                "memory.out",
                dest,
            ),
        )

    @classmethod
    def store_to_addr_at_pc(cls, src: str) -> list[instruction_step.InstructionStep]:
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
        steps: list[instruction_step.InstructionStep],
    ) -> frozenset[controller.Controller.Entry]:
        reset_control = "controller.instruction_counter.reset"
        increment_control = "controller.instruction_counter.increment"
        last_control = reset_control if reset_instruction_counter else increment_control
        steps = steps or [instruction_step.InstructionStep()]
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
