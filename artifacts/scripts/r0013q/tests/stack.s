.syntax unified
.arm
.text
.global __entry_fixture
.type __entry_fixture,%function
__entry_fixture:
    b fixture_caller
.size __entry_fixture, .-__entry_fixture

.type fixture_caller,%function
fixture_caller:
    str lr, [sp, #-8]!
    bl OUTLINED_FUNCTION_0
    ldr lr, [sp], #8
    bx lr
.size fixture_caller, .-fixture_caller

.type irq_unreachable,%function
irq_unreachable:
    str lr, [sp, #-8]!
    bl OUTLINED_FUNCTION_0
    ldr lr, [sp], #8
    bx lr
.size irq_unreachable, .-irq_unreachable

.type OUTLINED_FUNCTION_0,%function
OUTLINED_FUNCTION_0:
    mrc p15, 0, r0, c13, c0, 3
    bx lr
.size OUTLINED_FUNCTION_0, .-OUTLINED_FUNCTION_0
