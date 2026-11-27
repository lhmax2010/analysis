# 0013ae — Thumb-2 kernel: the full error inventory is in. Write the patch.

**Evidence (archive under `artifacts/evidence/`):** `native-run-r0013x-enum-stooH5-20261127.txt`, sha256 `eca2a767d23ebed37c82ce5cb4cdc76ade6414a49c206793cbd58446149291cf`. It contains the transcript plus the decoded JSON, whose sha256 is `6745cbb6…` and matches `ENUM_JSON_SHA256`.

## Result (pin `9569799`, run `stooH5`)

- `ENUM_RESULT COMPLETE`, gbs_exit 1, `make_k_seen true`: both keep-going passes ran.
- Thumb-2 config proven (`CONFIG_THUMB2_KERNEL=y` and `CONFIG_UNWINDER_ARM=y`; `.config` sha `9a07c28a…`).
- Product substituted to 37777148's 20261125.1; both build dependencies were found there.

**The complete compile-stage inventory is 10 errors, 8 distinct instruction sites, in 2 VDLinux-modified files.** Every other directory compiled under `make -k`.

| # | File / macro (caller) | Instruction | T32 problem |
|---|---|---|---|
| 1 | `arch/arm/lib/backtrace-clang.S:19`, `asm_store_regs_values` | `stmia r0, {r0 - r15}` | SP and PC are not allowed in a T32 STM list |
| 2 | `entry-armv.S`, `check_overflow` (from `__dabt_svc`, line 375) | `mov r8, sp, lsr #12` | SP cannot be a shifted operand |
| 3 | same | `eor r8, r8, sp` | SP is not allowed as a data-processing operand |
| 4 | same | `sub sp, r7, #(80 + 8)` | T32 `SUB SP, Rn, #imm` requires Rn = SP |
| 5 | same | `ldmia sp, {r0 - pc}^` | no exception-return LDM in T32 |
| 6 | `entry-armv.S`, `check_extension` (from `__irq_svc`, line 390) | `mov r8, sp, lsr #12` | as #2 |
| 7 | same | `eor r8, r8, sp` | as #3 |
| 8 | same | `sub sp, r7, #8` | as #4 |

All 8 are in Samsung's small-kernel-stack code (`CONFIG_KERNEL_STACK_SMALL`: stack overflow detection and stack extension) and its register-dump helper. Mainline code is not involved.

**INFO:** the build root also logs `find: command not found` and `xargs: command not found` from `gcc-warning-build-env.post` and `/usr/bin/gcc-force-options-only`. Check whether the same lines appear in the K0/K1 and jEMVH7 logs. If they do, the problem is pre-existing and only needs recording. If they don't, explain the difference, because the SERET-UL GCC step depends on that script.

## Task — the patch (workspace only; nothing to P4 yet)

1. **Rules for all 8 sites:**
   - Use mainline-style `ARM()` / `THUMB()` (or `W()`) variants, so that the **A32 build is byte-identical**.
   - Use only registers the surrounding code already saves and restores. Document each scratch register choice against the macro's save/restore sequence (r7, r8 and r9 at `[r0, #12/16/20]`).
   - Follow mainline's exception-return idiom for Thumb-2 for #5, as in `svc_exit` / `__dabt_svc`. Do not invent one.
   - For #1, a `.arm` function is acceptable if every caller reaches it through an interworking `BL`/`BLX` and it returns with `bx lr`. Otherwise, use a T32 sequence that stores r0–r12, then SP, LR and PC separately. Preserve the `pt_regs` layout and the exact values stored, especially what "PC" means to the caller.
2. **A32 identity control (required).** Rebuild K1 (A32, MLGO, `-moutline`) with the patch and the substituted product. Prove that:
   - `entry-armv.o` and `backtrace-clang.o` are byte-identical (`.text` hash);
   - vmlinux `.text` is still 8,214,312 B with 20,324 helpers.

   Also rebuild **unpatched** K1 once with the substituted product, to separate the product swap from the patch. Both may run in one session.
3. **Thumb-2 builds.** Build K4 (Thumb-2, MLGO) and K5 (Thumb-2, MLGO, `-moutline`) to completion: link, Image, zImage and the RPM.
   - Report `.text`, Image, zImage and helpers against K0 and K1.
   - List any **new link-stage errors or warnings**: veneers, relocation range, `.ARM.exidx`, `__ex_table`, interworking.
   - The compile inventory above does not cover the link stage.
4. **Static review of the Thumb-2 kernel.** Repeat the relevant 0013m checks for Thumb-2: S1 entry, vectors, idmap and MMU-off code in the right state; the exception vector stub mode; S4 fault tables; S9 thunks; S11 privileged instructions. Add a check that every exception entry and return path assembles to the intended state.
5. **Board test plan for the patched paths.** These handlers run only when the kernel stack nearly overflows, or when an IRQ arrives on a small stack. Propose a test that actually executes `check_overflow` and `check_extension` on the board, such as a debug module or a deliberate deep recursion under `CONFIG_KERNEL_STACK_SMALL`, and checks recovery and `do_stackoverflow` reporting.
6. **Deliverable for the TEST-ONLY shelf** (the operator shelves it, the PM writes the command): the exact file list and sha256s on top of shelf 14427407.
   - The 2 assembly files.
   - The KANTSU2E perf defconfig change that enables Thumb-2. Should debug and release follow too? Advise.
   - The spec, only if needed.

   The Thumb-2 kernel QB is MLGO without `-moutline`, so that each change is measured separately; the combination comes later.

Give the PM hash-pinned native commands for steps 2–3. They use the existing locks and resource checks, and the same `PRODUCT_URL` default.

No GitHub submission from the Native Server.
