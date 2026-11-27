### Decision 0013n

The user authorizes Product, kernel and LLVM changes as reviewed TEST-ONLY shelves. Each CL is pending, starts with `[TEST ONLY - DO NOT SUBMIT]`, and is tested from the shelved contents in GBS and QuickBuild. Claude reviews the diff, SHA-256 and shelf command first. This supersedes the earlier LLVM-only restriction. [Decision](../../decisions/DECISIONS.md) · [PM original](../claude_to_codex/0013n_codex_policy_shelve_and_thumb2_kernel.md)

### Enumerate errors for the K4 configuration

```bash
(
set -eu -o pipefail
p=9e8886d877244b9a75d16f6fa1a8f3fae734c600
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013n-launch.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0013n/enumerate.sh.txt" -o "$d/run"
printf '%s  %s\n' 967b647bf999efac338f62dd955d5f24e61be1978c89e564d08cb3453082f9f4 "$d/run" | sha256sum -c -
bash "$d/run" "$p" | tee "$d/combined.txt"
)
```

Native server, attended under the existing kernel locks. The retained dkyJ0S K4 source and GBS config are read-only inputs. The command creates a fresh workspace clone of the exact staged K4 revision and its own GBS root. It runs the production kernel recipe with make keep-going and repeats a failed make invocation to expose remaining reachable diagnostics. It checks the generated THUMB2_KERNEL and UNWINDER_ARM settings. Budget 105 GiB free, 32 GiB available RAM and six cores. Allow 30–120 minutes, possibly longer for the second pass. It uses sudo for the ordinary GBS build. No P4 workspace edits.

Return ENUM_INPUT, ENUM_RESULT, the SITE lines and ENUM_PART packets. If more than four packets are needed the command prints the exact packet path. Print one line per paste with the indicated sed command, increasing the line number. The packet includes the exact diagnostics, macro notes, file origins versus upstream v6.12.60 where retrievable, and source context for patch review. A failed prerequisite can prevent downstream link diagnostics; repeat after fixing those prerequisites.

### Current patch and measurement status

The retained transcript proves two blockers. One compiler invocation was previously attempted out of 84 candidates. No complete failure census or patched K0/K4/K5 result is available. The native GBS checkout and its build roots are not mounted on the PC.

| Site | Existing evidence | Patch criterion |
|---|---|---|
| arch/arm/lib/backtrace-clang.S:19 | VDLinux-modified; Thumb rejects SP and PC in `stmia r0, {r0 - r15}`. | Preserve every saved GPR slot and diagnostic PC meaning. Keep original ARM instruction under ARM(). Review local scratch register, LR, flags and the saved PC convention before selecting the THUMB() sequence. |
| arch/arm/kernel/entry-armv.S:375, check_overflow invocation | Compiler rejects `mov r8, sp, lsr #12` in this Thumb build. The macro definition needs the source context. | In a local ARMv7-A ISA fixture, `lsr.w r8, sp, #12` was rejected. `mov r8, sp` followed by non-flag-setting `lsr.w r8, r8, #12` assembled. Preserve flags and the macro's actual shift constant. |

The patch diff, patched local build and P4 shelf commands follow the enumeration return as requested in §3. They depend on the actual file set and source-level register semantics. Acceptance requires exact K0 vmlinux .text bytes against the control, K4 vs K0 and K5 vs K1 uImage/Image/zImage sizes, .text/.rodata/.data/.bss/allocated .init.*, separate .ARM.exidx/.ARM.extab, mapped A32/T32 and unknown bytes, helper counts, actual compiler argv and the effective configs. Include the Thumb config and assembly changes in the first Official test shelf. The optional K5 QB adds only the separately verified Clang outlining treatment.

### Board sequence after local qualification and flash review

Verify the Official rollback USB and its manifest, record build ID and boot slot, then compare Official with the Thumb-only candidate on the same KantSU2E. Run five boots, suspend/resume and fast boot. Exercise display, audio, USB, network, remote input and signed 4K playback. Record frame drops, CPU, PSS/USS, available memory, logs and a 24-hour soak. Verify diagnostic unwind quality using the previously approved owner fixture. For kernel/user interworking, exercise syscalls from both signed ARM and Thumb userspace programs, check signal handler delivery and return, check vectors/kuser page placement and exercise the vDSO time path if present. Record mapping, functional result and workload identity; unavailable probes remain open. Confirm BOOST rollback and stop at the first boot, unwind, interworking or peripheral failure. Repeat against K5 only after K4 acceptance. [Runtime gates](0013jk_reply.md)
