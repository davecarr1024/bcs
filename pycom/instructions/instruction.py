import dataclasses
import typing
from pycom.components import controller, errorable
from pycom.instructions import step as step_lib
from pycom.programs.operands import operand
from pycom.programs import statement


@dataclasses.dataclass(frozen=True, kw_only=True)
class Instruction(errorable.Errorable):
    class OperandInstanceNotFound(errorable.Errorable.Error, KeyError): ...

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class OperandInstance:
        @dataclasses.dataclass(frozen=True, kw_only=True)
        class StatusInstanceKey:
            status_mask: int = 0
            status_value: int = 0

        @dataclasses.dataclass(frozen=True, kw_only=True)
        class StatusInstance:
            steps: list[step_lib.Step]

            def entries(
                self,
                *,
                opcode: int,
                status_mask: int = 0,
                status_value: int = 0,
            ) -> frozenset[controller.Controller.Entry]:
                preamble = Instruction._preamble()
                return preamble | Instruction._entries_for_steps(
                    instruction=opcode,
                    starting_instruction_counter=len(preamble),
                    reset_instruction_counter=True,
                    steps=self.steps,
                    status_mask=status_mask,
                    status_value=status_value,
                )

        opcode: int
        status_instances: dict[
            StatusInstanceKey,
            StatusInstance,
        ] = dataclasses.field(default_factory=dict)

        def with_status_instances(
            self,
            status_instances: dict[
                StatusInstanceKey,
                StatusInstance,
            ],
        ) -> "Instruction.OperandInstance":
            return Instruction.OperandInstance(
                opcode=self.opcode,
                status_instances=self.status_instances | status_instances,
            )

        def with_status_instance(
            self,
            *,
            status_mask: int = 0,
            status_value: int = 0,
            steps: list[step_lib.Step],
        ) -> "Instruction.OperandInstance":
            return self.with_status_instances(
                {
                    self.StatusInstanceKey(
                        status_mask=status_mask, status_value=status_value
                    ): self.StatusInstance(
                        steps=steps,
                    )
                },
            )

        @classmethod
        def build(
            cls,
            *,
            opcode: int,
            status_mask: int = 0,
            status_value: int = 0,
            steps: list[step_lib.Step],
        ) -> "Instruction.OperandInstance":
            return Instruction.OperandInstance(
                opcode=opcode,
            ).with_status_instance(
                status_mask=status_mask,
                status_value=status_value,
                steps=steps,
            )

        def entries(self) -> frozenset[controller.Controller.Entry]:
            return frozenset().union(
                *[
                    status_instance.entries(
                        opcode=self.opcode,
                        status_mask=key.status_mask,
                        status_value=key.status_value,
                    )
                    for key, status_instance in self.status_instances.items()
                ]
            )

        def statement(self, operand: operand.Operand) -> statement.Statement:
            return operand.statement(self.opcode)

    operand_instances: dict[
        typing.Type[operand.Operand],
        OperandInstance,
    ] = dataclasses.field(default_factory=dict)

    def entries(self) -> frozenset[controller.Controller.Entry]:
        return frozenset().union(
            *[instance.entries() for instance in self.operand_instances.values()],
        )

    def operand_instance(
        self, operand_type: typing.Type[operand.Operand]
    ) -> OperandInstance:
        if operand_type not in self.operand_instances:
            raise self.OperandInstanceNotFound(
                f"instruction {self} doesn't accept operand type {operand_type}"
            )
        return self.operand_instances[operand_type]

    def statement(self, operand: operand.Operand) -> statement.Statement:
        return self.operand_instance(type(operand)).statement(operand)

    def with_operand_instances(
        self,
        operand_instances: dict[
            typing.Type[operand.Operand],
            OperandInstance,
        ],
    ) -> "Instruction":
        return Instruction(
            operand_instances=self.operand_instances | operand_instances,
        )

    def with_operand_instance(
        self,
        operand_type: typing.Type[operand.Operand],
        operand_instance: OperandInstance,
    ) -> "Instruction":
        return self.with_operand_instances({operand_type: operand_instance})

    def with_instance(
        self,
        *,
        opcode: int,
        operand_type: typing.Type[operand.Operand],
        steps: list[step_lib.Step],
        status_mask: int = 0,
        status_value: int = 0,
    ) -> "Instruction":
        return self.with_operand_instances(
            {
                operand_type: self.OperandInstance.build(
                    opcode=opcode,
                    status_mask=status_mask,
                    status_value=status_value,
                    steps=steps,
                ),
            }
        )

    @classmethod
    def build(
        cls,
        *,
        opcode: int,
        operand_type: typing.Type[operand.Operand],
        steps: list[step_lib.Step],
        status_mask: int = 0,
        status_value: int = 0,
    ) -> "Instruction":
        return Instruction().with_instance(
            opcode=opcode,
            operand_type=operand_type,
            steps=steps,
            status_mask=status_mask,
            status_value=status_value,
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
