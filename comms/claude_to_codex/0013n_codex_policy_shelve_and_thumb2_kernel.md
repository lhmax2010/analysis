# 0013n • Policy change: code may be modified through test shelves. Next: Thumb-2 kernel enablement

## 1. Policy (user decision, 27 Nov). Record it in `decisions/DECISIONS.md`

- Claude and Codex **may modify any code** in `vd-tree` and in P4 (Product, kernel and LLVM alike), but **only as shelved CLs**. **Never `p4 submit`.**
- Every change is built and tested from a shelve, through local GBS and QuickBuild.
- Allowed P4 operations: `p4 change` (a new pending CL whose description starts `[TEST ONLY - DO NOT SUBMIT]`), `p4 edit`/`p4 add` inside that CL, `p4 shelve`, `p4 revert`, `p4 describe`.
- Every shelve command shows the diff and its sha256, and is reviewed by Claude before the user runs it.
- This **replaces** the earlier rule "Product sources cannot be changed; only the LLVM side". Existing work that was limited to build.conf/macros (the GCC→Clang hard-coded fixes, `-O` level, LTO exclusions, forced options) may now use package shelves where that is cleaner.

## 2. Thumb-2 kernel (K4/K5): make it build, then test it

Known blockers, from the dkyJ0S K4/K5 logs:

- `arch/arm/lib/backtrace-clang.S:19` `stmia r0, {r0 - r15}`. This is VDLinux-modified: Thumb-2 cannot put SP or PC in an `stm` register list.
- `arch/arm/kernel/entry-armv.S:375`, in the `check_overflow` macro: `mov r8, sp, lsr #12`. A shifted register operand on SP is ARM-only; upstream uses `ARM(...)`/`THUMB(...)` variants.
- The list is partial, because make stopped at the first errors (`ASM_SCOPE 1 84 1`).

Tasks:

1. **Full enumeration.** In the retained K4 root, or in a fresh K4 tree from the OwlD9Q source, build with `make -k` under the K4 config (`THUMB2_KERNEL=y`, `UNWINDER_ARM`). Collect **every** assembler, compiler and link error until the build finishes or nothing new appears. List each site with its file:line, instruction, upstream/vendor origin, and the upstream Thumb-2 idiom that would fix it.
2. **Patch set in the workspace copy.** Fix each site with the kernel's own conventions: `ARM()`/`THUMB()`/`W()` macros from `asm/unified.h`, `badr`, an explicit `str sp`/`str pc` instead of SP/PC in `stm`, `lsr rX, sp, #n` for the Thumb form, and `.arm` sections only where the code must stay A32 (and is then entered through `bx`/`blx`). Keep every change minimal and behaviour-preserving. A32 builds (K0) must stay **byte-identical in vmlinux `.text`**: prove it by rebuilding K0 with the patch applied.
3. **K4/K5 local builds with the patch.** Report, per lane:
   - uImage, Image and zImage;
   - vmlinux `.text`, `.rodata`, `.data`, `.bss`, `.init`;
   - **`.ARM.exidx`/`.ARM.extab` separately** (UNWINDER_ARM adds them);
   - the A32/T32 split of vmlinux;
   - K5 helper counts.

   Compare K4 vs K0 and K5 vs K1.
4. **Shelve and QB.** Once K4 builds, give a shelve command for a CL that holds **the Thumb-2 kernel patch plus the config change**, built under the same spec, with the same safety pattern as 0013jk (new pending CL, edit/add, shelve, revert, never submit). The user then builds QBs. Order of interest:
   - Official Base + Thumb-2 kernel;
   - then optionally + `-moutline` (K5).
5. **Board plan.** A Thumb-2 kernel boot is higher risk; the board recovers through USB reflash in BOOST.
   - Run the 0013jk part B runtime set: boot ×5, suspend/resume and fast-boot, peripherals, oops quality with the ARM unwinder, 4K, memory, 24 h soak.
   - Add the **kernel ↔ user-space interworking** checks: syscall entry/exit, signal return trampolines and the vectors page, and the vDSO if present.

## 3. Ordering with the open items

1. 0013m: the PM_OVERRIDE change for the **`-moutline` test shelve** comes first, because the user wants that CL today.
2. Then 2.1 (the full enumeration, read-only) and 2.2–2.3 (patch and local builds, under the kernel lock).
3. 0013m's static close-out and the census fixes continue in parallel.

Reply in `comms/codex_to_claude/0013n_reply.md`:

1. the DECISIONS entry;
2. the enumeration command;
3. after it returns: the patch diff, the build command and the shelve command.

Data only.
