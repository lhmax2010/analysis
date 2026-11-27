# 0013ae · Native commands for PM review

**1. A32 control.** Run in an attended Bash terminal on the native GBS host. This builds K1 twice, first from the original shelf, then with the three source edits and the original A32 configuration. Keep this shell open for step 2.

```bash
pm13ae() (
  set -eu -o pipefail
  pin=086b2463adb5e2d06733152e0df230f474b3e3e3
  t=/home1/chengkai/vd-tree/workspace/temp
  d=$(mktemp -d "$t/pm0013ae-get.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013ae/run.sh.txt" -o "$d/run.sh"
  printf '%s  %s\n' a945cb8acfba63e9bb8d4fd226edf355e4ceea7fa9f273238554c8d02f77b08b "$d/run.sh" | sha256sum -c -
  bash "$d/run.sh" "$pin" "$@"
)
pm13ae control
```

**2. K4 and K5.** Paste the absolute `identity.json` path from step 1's `A32_RECEIPT` line at the prompt. The launcher verifies the receipt inputs and the hashes of both measurement files before GBS starts. K4 is perf with Thumb-2 and MLGO. K5 adds the Clang machine outliner. Each must finish linking, packaging and zImage verification against the perf RPM before its measurement is reported.

```bash
read -r -p 'Absolute identity.json path from A32_RECEIPT: ' receipt && pm13ae thumb "$receipt"
```

Both use the retained stooH5 input revision `fae92f998a51e8493e2ed452381aad73c2ce689e` (14293732 plus shelf 14427407), the K4 repository configuration with the LLVM Official 37777148 Product substitution (20261125.1), and the pinned Official published build.conf. Leave `PRODUCT_URL` unset to use that substitution. The same settings must be used for both commands. One GBS build runs at a time under the three existing heavy locks, with up to six CPUs and an attended sudo prompt. Admission is 105 GiB free and 32 GiB available RAM before **each** lane. Roots are retained. Allow several hours per pair as a scheduling estimate. Network use comprises pinned script downloads and GBS repository traffic on cache misses.

## What the native readback establishes

The native operator materialized the following four files against 14427407. The full unified patch is 5,454 bytes. Its SHA-256 is `4c9dc96ac05db07715f297d359b7180f01a51332472843dba6fef59796852368`. The build launcher checks each full-file hash while staging. [Patch](../../artifacts/patches/kernel/thumb-small-stack.patch) · [Operator transcript and encoded patch](../../artifacts/evidence/operator-r0013ae-read-3rWNs0-20261127.txt)

| TEST shelf path, relative to linux-6.12/ | SHA-256 after the change |
|---|---|
| arch/arm/kernel/entry-armv.S | `df3f874af40e76b796c1dd8435bd17fd2f0e39c677344a09990d3b573316f04d` |
| arch/arm/lib/backtrace-clang.S | `0761192a9336e2c06b8034b96d53cb5c3d7f4787174e7d705a9a44fa37b95e0a` |
| arch/arm/kernel/traps.c | `ced2d314a4c2eb6834cbb8c4cfeb6b8e5306c95cca627053af0a01d31ef5a595` |
| arch/arm/configs/KANTSU2E_perf_defconfig | `d9ef5d653eee71aae4ead4810457652e5b0e3ec1f120b14245997bb6c4a4480f` |

The proposed TEST shelf is K4, with MLGO enabled. It needs no spec edit. The local measurement spec supplies instrumentation and the K1/K5 outliner treatment. Keep debug and release defconfigs at their existing settings until their own configuration and runtime evidence is available. Shelf creation and board acceptance are pending.

stooH5 enumerated 10 compile diagnostics at eight instruction sites across two files. Its keep-going build exited 1. In each of K0, K1, jEMVH7 and stooH5 the top-level log contains one missing `find` and two missing `xargs` in `gcc-warning-build-env.post`, plus five missing `find` in `gcc-force-options-only`. Each package log repeats the same counts. These diagnostics predate the Thumb port and also occur in the successful K0 and jEMVH7 package builds. [Enumeration](../../artifacts/evidence/stooH5-enumeration-20261127.json) · [Original transcript](../../artifacts/evidence/native-run-r0013x-enum-stooH5-20261127.txt)

## Exception return and register review

| Site | Register and state contract |
|---|---|
| Both page-offset and IRQ-stack checks | The macros save r7/r8 at offsets 12/16 from r0. Copy SP to r8 before the shift, preserving the rounded DFAR in r7 in the overflow path. For XOR, r7 already contains the IRQ-stack bottom. Copy SP into r8 and XOR with r7. The slow path saves r9 at offset 20 before using it. |
| Switching stacks | Save the interrupted SP in r8. Subtract the frame size in r7, then move it into SP. The extension path restores the IRQ-stack top to r7 for cleanup after the call. The overflow path reloads r7 from the exception frame. |
| Backtrace register dump | The Thumb build uses a word-aligned A32 function containing the original register store and an explicit `bx lr`. The 16 words retain r0–r12, SP, LR and the A32 instruction's architectural stored PC at offsets 0–60. The linked-image check inventories callers, their instruction states and the actual callee body. |
| do_stackoverflow | In Thumb builds a successful return supplies the mapped page base B, after installation of the page and the pointer at its first word. If the failure path returns from `die()`, it supplies NULL. The original A32 declaration and return remain under the complementary condition. Original register values are already in the IRQ-stack frame when the caller uses r0 (B), r2 (difference), r5 (saved PSR) and LR (scratch). |

Let P be the saved SP. The ordinary Thumb tail requires a non-NULL B, word alignment of P, unsigned P ≥ B, and **16 ≤ P − B ≤ PAGE_SIZE**. It stages LR at [P−12,P−8), PC at [P−8,P−4) and PSR at [P−4,P). This keeps all three words within the newly mapped page and preserves [B,B+4), which holds the page pointer. The tail pops LR and then uses RFE to consume PC and PSR. Its other frame accesses use the IRQ stack. The Thumb sequence follows the target's `svc_exit` register-restore fragment. [Linux ARM entry header](https://github.com/torvalds/linux/blob/v6.12/arch/arm/kernel/entry-header.S)

For NULL, misalignment, or a range outside the guard, that 12-byte write has no established safe destination. The boundary path loads the even address of a dedicated `.arm` function and executes `bx lr`. It restores the saved SPSR from r5 and executes exception-return LDM from the IRQ frame. This restores CPSR including the saved T bit and retrieves the original SP directly. The fixture emitted the following code and an ARM unwind entry marked `cantunwind` for the island.

```text
0x04  msr SPSR_fsxc, r5
0x08  ldm sp, {r0-r12, sp, lr, pc} ^
0x46  rfeia sp!
0x4a  adr.w lr, #-72       @ even target 0x04
0x4e  bx lr
0x50  stm r0, {r0-r12, sp, lr, pc}
0x54  bx lr
```

Local checks cover Python 3.10, the pinned dependency manifest, Bash 3.2 syntax for the generated wrappers, and assembly/disassembly of the patched instruction fixtures. For caller proof the native launcher runs source-wide `git grep`, records object relocations, and checks the linked branch to `do_stackoverflow` from `__dabt_svc`. Review any non-call references in `reference-review.tsv`, including possible address-taken uses. The whole-kernel cross-reference and final disassembly await the builds.

## Measurement and static gates

| Historical reference, bytes | vmlinux .text | raw Image | zImage | Outlined helpers |
|---|---:|---:|---:|---:|
| K0 / Official | 8,564,600 | 11,348,644¹ | 5,326,464 | 0 |
| K1 | 8,214,312 | 10,996,388 | 5,449,312 | 20,324 |

¹ Official raw-image reference used for the K0 delta. The zImage column uses the replay. The matched Official QB zImage is 5,326,504 bytes.

The first command compares **both whole-object SHA-256 and executable-section hashes** of `entry-armv.o`, `backtrace-clang.o` and `traps.o`, the effective configs, and the exact K1 .text and helper count. The second prints K4 and K5 measurements and deltas to both historical references. New lane sizes, link warnings and runtime results await operator execution.

Inspect S1 (vectors, entry, idmap, MMU-off and indirect edges), S4 (fault-table entries and targets), S9 (thunks, interworking and dump callers), S11 (privileged instructions in helpers), and the explicit entry/return state inventory. The conservative S1/entry verdict calls for human review of indirect control flow, even if the dedicated return check passes. Use the following compact terminal readback after the second command. The full files remain in its WORKDIR.

```bash
(
set -eu
read -r -p 'Absolute pm0013ae-thumb WORKDIR: ' work
for lane in K4 K5; do
  for file in source-xrefs.txt overflow-callers.tsv dump-callers.tsv dump-body.tsv restore-paths.tsv link-diagnostics.txt static.json; do
    p="$work/$lane/$file"
    printf '%s %s\n' "$lane" "$file"
    if test -f "$p"; then head -n 14 "$p"; else printf 'MISSING\n'; fi
  done
done
)
```

## Board verification after PM reviews both linked kernels

Use an engineering image with source-level trace or hardware instruction trace and a controlled workload in a user task's syscall context. A plain kernel thread can take the `_TIF_VM_KTHREAD` exemption. Record the kernel build ID, active config, original PC/SP/LR/PSR, mapped page and task, the branch taken and progress after exception return. Keep test instrumentation separate from the four-file shelf.

| Case | Observation required to count the case |
|---|---|
| IRQ on a near-limit task stack | Observe `check_extension` taking its slow branch, the call to `do_stack_extension`, return from IRQ, and subsequent task progress. |
| Normal overflow return | Correlate the task's `[STACK EXTENDED]` messages with successful mapping, the guarded P−B range, execution of `pm_stack_thumb_restore` and RFE. Check restored SP, LR, PC, T bit and page-first pointer. |
| Boundary return | Obtain a genuine outer-range saved SP with a valid interrupted context. Correlate mapping, `pm_stack_boundary_switch`, the A32 island and resumed task. Check the same saved state and the first word. A branch count alone is insufficient evidence of recovery. |
| Returning failure | On a separate diagnostic image, a test hook may return NULL after a safe successful mapping to exercise dispatch and recovery. Record this as a simulated NULL return. If scoped allocator fault injection is available, record the actual `do_stackoverflow` failure and terminal or recovery outcome separately. A fatal `die()` provides no returning-failure measurement. |

A route with no trace stays untested. Stop the run on a state or pointer mismatch and retain the trace for review. No board measurements or P4 shelf have been reported in this round.
