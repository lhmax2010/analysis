# 0013jk • Kernel -moutline: side-effect verification (part 1), then a test shelve for two QBs (part 2)

This is one prompt in two parts. Do part 1 first: it gates part 2. Reply in a single file, `comms/codex_to_claude/0013jk_reply.md`, with the part 1 command first and the part 2 sections after it.

---

## PART 1


The size result is final:

| Pair | `.text` change |
| --- | --- |
| K1 vs K0 | −350,288 B (−4.09%) |
| K3 vs K2 | −489,252 B (−4.96%) |

zImage changes by +2.31% and +2.56%, and K1 has 20,324 helpers totalling 316,380 B (source: the `pm0013i-read.a0Pmc0` receipt `f7f1148e…`, both ARGV PASS).

HQ is worried about **side effects**. Verify everything that can be verified statically from the retained K1/K3 build trees (`vmlinux`, `System.map`, objects and `.cmd` files) now, read-only, and prepare the runtime part for the board. No build lock, no GBS, idle I/O. It may run in parallel with the running `0013i` command 1.

## A. Static checks (K1 vs K0, K3 vs K2)

| # | Side effect | Method | Pass rule |
| --- | --- | --- | --- |
| S1 | **Section placement and boot-critical code** | For every `OUTLINED_FUNCTION_*`, record its section and every caller's section. Flag calls from `.head.text`, `.idmap.text` (MMU-off identity map), `.entry.text`, `.noinstr.text`, `.init.text`/`.exit.text` into helpers placed elsewhere (or the reverse), plus `.hyp*`, `.cpuidle.text`, `.kprobes.text`, `__exception_text`, `.vectors`/`.stubs`, suspend/resume and cache/TLB maintenance paths. | Zero helpers reached from MMU-off, idmap, vector or entry code. Any cross-section call is listed with its caller. |
| S2 | **Outlined call variants and stack use** | Classify every call site by variant: tail call, thunk, no-LR-save, register save, stack save (the `push {lr}` wrapper). Count the stack-save sites, and the maximum extra stack per call chain (static estimate, against the 8 KiB ARM32 kernel stack). | Report the counts. No stack-save variant inside IRQ, entry or exception paths. |
| S3 | **Unwinding and backtrace** | K1/K0 use `UNWINDER_FRAME_POINTER`. Check that helpers never set up or modify `fp`/`r11` frames, and that callers keep their frame record across the helper call. Disassemble a sample of 20 helpers by variant. | A frame-pointer walk through any helper still reaches the true caller (static argument, then the board test in B). |
| S4 | **Exception tables and fixups** | Check that no instruction covered by `__ex_table` (user-access fixups) or `__bug_table`/`WARN` sites was moved into a helper, so that the fault-PC → fixup lookup still works. Compare the entry counts and verify that every fixup insn address lies in a non-outlined function. | Zero fixup or bug-table addresses inside `OUTLINED_FUNCTION_*`. |
| S5 | **Atomics and exclusive monitors** | Make sure no helper contains `ldrex`/`strex` sequences split from their loop, or barriers (`dmb`/`dsb`/`isb`) whose ordering depends on the caller context. | Zero split exclusive pairs; any barrier inside a helper is listed. |
| S6 | **Instrumentation and debug interactions** | perf config: `FTRACE`, `KPROBES`, `KALLSYMS` and stack protector are off. State which debug or other configs would interact (mcount/fentry absence in helpers, kprobe blacklist, kallsyms names, stack protector canaries). | Documented; a gate for any config that enables them. |
| S7 | **External modules and the GCC part** | SERET-UL and external modules are built by GCC without `-moutline`. Confirm that module-facing exported symbols (`__ksymtab`, CRCs) and the module ABI are unchanged K1 vs K0. | `Module.symvers` / ksymtab identical apart from addresses. |
| S8 | **Code layout and I-cache** | Helper size distribution, number of distinct callers per helper, and hot-path exposure: the share of outlined sites in `sched/`, `mm/`, `net/core`, `fs/`, `drivers/media`, irq/entry. | Report the numbers; they feed the performance gates in B. |

## A2. Further side-effect scenarios added by PM (static, same command)

| # | Side effect | Method | Pass rule |
| --- | --- | --- | --- |
| S9 | **Long-branch veneers** | The ARM `BL` range is ±32 MiB, and outlining adds BLs. Count the lld range-extension thunks (`__ARMv7ABSLongThunk_*`, `__ARMV7PILongThunk_*`, `*LongThunk*`) in K1 vs K0 and K3 vs K2: number, bytes, and where they sit. | Thunk growth reported; no thunk inside idmap, entry or vector sections. |
| S10 | **PC-relative literals** | Make sure no helper holds a PC-relative load (`ldr rX, [pc, #…]`, `adr`) that refers to a literal pool belonging to a caller. | Zero. |
| S11 | **System-state instructions** | No helper may contain `mrs`/`msr` (CPSR or SPSR), `cpsid`/`cpsie`, `mcr`/`mrc` (CP15 cache, TLB or MMU), `wfi`/`wfe`, `svc`, or `setend`. Outlining these would move IRQ masking or MMU/cache control out of their context. | Zero, or each one listed with its callers. |
| S12 | **In-tree modules** | In-tree `.ko` files are Clang-built and also get outlined. Compare each `.ko`'s size, its `OUTLINED_FUNCTION` count, and its relocation types (`R_ARM_CALL`/`JUMP24` and any new type) against what the module loader supports. Module PLT needs: K1 vs K0. | Only relocation types the loader handles; size delta reported. |
| S13 | **Debug info coverage** | Check that `.debug_line` and `.debug_info` cover the helper addresses, so that oops PCs inside a helper still resolve to a source file and line (`addr2line`/crash tool). | Coverage percentage reported; gaps listed. |
| S14 | **Profiling attribution** | perf samples that land in a helper are charged to `OUTLINED_FUNCTION_n`, not to the real function. Estimate how much hot-path time is affected; this also matters for our own P1 profiling. | Documented, with a mitigation (map helpers to their callers). |
| S15 | **Timing-sensitive vendor drivers** | Identify the share of outlined sites in `drivers/samsung`, NVT/SoC drivers, I2C/GPIO/SPI bit-banging, IR/CEC, tuner and display paths. A call and return inside a timed register sequence adds latency. | List the drivers with outlined sites inside `udelay`/`ndelay` or MMIO sequences. |

## B. Runtime side effects (needs a bootable K1 kernel)

Runtime items added by PM (besides boot, benchmarks, 4K and soak):

- **suspend/resume and TV fast-boot/instant-on** ×5, because the resume path runs with the MMU or caches in a special state;
- a **peripheral smoke test**: remote/IR, HDMI-CEC, tuner/channel change, Wi-Fi, BT, USB, audio;
- **watchdog and lockup** messages during the soak;
- **oops quality**: a real backtrace through a helper, symbolized with addr2line or crash.

Prepare the runbook. Whether we can execute it depends on whether KantSU2E PERF accepts a locally built kernel (the user is confirming this). On the same board, compare K0 (local build, same source) with K1 (local build) with alternating boots:

- boot to Home ×5;
- a **deliberate `WARN`/oops path** (a QA trigger, only if one exists without a source change) for backtrace quality;
- `hackbench` / `perf bench sched` / `perf bench mem` if signed and available in the image;
- 4K playback ×3 (CPU load, dropped frames);
- MemAvailable at Home;
- 24 h soak (no new oops, panics or warnings in `dmesg`).

If local kernels cannot boot, list exactly what a signed QB kernel needs (spec/config delta, clang-only `KCFLAGS`) so that HQ can produce it.

## C. Additions to the Thumb-2 user-space gates (0013g), found by PM

| # | Side effect | Method | Pass rule |
| --- | --- | --- | --- |
| C7 | **Deprecated IT blocks on ARMv8 AArch32** | Clang targets `thumbv8a` with `-mimplicit-it=thumb`. In ARMv8, an IT block covering more than one instruction, or a 32-bit instruction, is deprecated: it is slow, and it is **UNDEFINED if `SCTLR.ITD`=1**. Count the deprecated IT forms in the Thumb ELFs, which come mainly from hand asm or inline asm. Then read `SCTLR.ITD` on the board, or from the kernel `proc-v7` setup source. | ITD=0 confirmed, and the deprecated-IT count reported per package; if ITD=1, every deprecated site is a blocker. |
| C8 | **Unaligned and doubleword accesses** | Thumb-2 code generation may use `ldrd`/`strd`/`ldm` on addresses whose alignment differs from A32 code. Check the kernel alignment-trap settings (`/proc/cpu/alignment` on the board) and count alignment fixups during the soak. | No new alignment fixups or SIGBUS. |
| C9 | **Mixed-mode C++ exceptions, setjmp/longjmp, signals** | On the board, run tests that throw and catch C++ exceptions across A32/T32 library boundaries, call `longjmp` across mixed frames, and use signal handlers in Thumb code with `ucontext`. | All pass on the Thumb QB. |
| C10 | **Core dump and gdb usability** | A Thumb core dump must be analysable: correct mode detection, `$t`/`$a` mapping symbols, a backtrace through mixed frames. | Correct symbolized backtrace. |

## Deliverables

Give one pinned read-only command for S1–S15, printing at most 40 lines with the full TSVs in an archive. C7 (static count) and C8 (static part) can go into the same command if the 0013i platform extraction has finished; otherwise put them in the next 0013g run. Add these tables to `reports/weekly/2026-11-27/draft-data.md`:

- a "Kernel -moutline side effects" table (S1–S15 results, B status);
- the C7–C10 rows in the Thumb-2 acceptance plan.

Part 1 output: the pinned read-only command, placed first in `0013jk_reply.md`. Data only.

---

## PART 2


**User decision:** KantSU2E PERF is tested with QB-built (signed) images. The user asks us to prepare a **shelved CL** (test only, never submitted) that adds `-moutline` to the Clang kernel build. The user will build **two QBs**: one on the Official Base and one on the Custom Base. Codex then tests them on the board against the existing pair.

| Image | Base | Kernel |
| --- | --- | --- |
| Official 37777148 (exists) | 20261113.1 | MLGO (official models) |
| **Official + outline (new QB)** | 20261113.1 | MLGO (official) + `-moutline` |
| Custom 37777264 (exists) | 20261118.1 | MLGO (custom models) |
| **Custom + outline (new QB)** | 20261118.1 | MLGO (custom) + `-moutline` |

## Tasks

1. **Minimal production change, without the measurement hooks.** Take the exact `packaging/tztv-kernel.spec` that the 37777148/37777264 QBs build: kernel CL 14293732 plus the existing kernel shelf 14427407, as in the retained manifest. Derive the smallest diff that passes `-moutline` **only to Clang compiles**, using the make conditional `$(if $(filter clang clang-% %-clang,$(notdir $(lastword $(CC)))),-moutline)` that 0013i proved. It must cover every Clang-built flavour and the in-tree modules, while SERET-UL and any GCC step get nothing.
   - None of the `perf-machine-outliner.spec.patch` evidence hooks may appear: no tools wrapper, no evidence copying, no `V=1`.
   - Show the full diff, which should be a few lines.
2. **Pre-QB verification build (local GBS, kernel lock, sudo).** Build the exact shelve content on the Official Base config, using the 37736448/37777148 published build.conf. The pass conditions are:
   - GBS exit 0, **including the SERET-UL/GCC step**;
   - the `tztv-kernel-perf` RPM is produced;
   - `.text`, Image and zImage are within noise of K1 (`.text` 8,214,312);
   - the helper count is about 20,324;
   - the effective argv proves `-moutline` on Clang compiles and its absence on GCC compiles.

   Give this as a pinned command. It reuses the OwlD9Q source and takes about 30 minutes.
3. **Shelve command for the user (native, attended).** Using the user's existing P4 client on the native host:
   - create a **new pending CL** with the description `[TEST ONLY - DO NOT SUBMIT] kernel: clang-only -moutline for KantSU2E perf (LLVM adaptation measurement)`;
   - `p4 edit` only the spec file;
   - apply the verified diff, and check its sha256;
   - run `p4 shelve -c <CL>`, then `p4 revert -c <CL>` locally;
   - print the CL number and `p4 describe -S -s <CL>`.

   **Never `p4 submit`.** The script must refuse if the client root or depot path differs from what you expect. Print the depot path you expect, so that the user can confirm it.
4. **QB submission notes for the user.** Use the same Product, the same build.conf (`98690f23…`) and the same shelf list as 37777148 and 37777264, **plus the new CL**: one QB on Base 20261113.1 and one on Base 20261118.1. Name what must be identical across all four images.
5. **Gate before the user submits the QBs:** the part 1 static checks S1, S4, S9, S11 and S12 must pass on the K1/K3 builds. Report them first.
6. **Board plan for the four images**, merged with part 1, section B:
   - kernel identity and sizes (`/proc/iomem`, boot Memory line);
   - boot ×5;
   - suspend/resume and fast-boot ×5;
   - peripheral smoke test;
   - scheduler and memory benchmarks;
   - 4K ×3;
   - MemAvailable at Home;
   - an oops-quality check;
   - a 24 h soak for each `+outline` image.

   Compare `+outline` against its own Base. MLGO-official vs MLGO-custom is a separate axis.

Part 2 output goes in `0013jk_reply.md` after the part 1 command, in this order:

1. the S1/S4/S9/S11/S12 verdicts;
2. the diff;
3. the pre-QB build command;
4. the shelve command;
5. the QB notes;
6. the board plan.

Data only. Part 2 comes after the part 1 static command.
