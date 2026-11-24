# 0012f • Official perf kernel outliner trial

**Current result: blocked on the effective Official perf configuration.** We have the source identity and source-level advisor switches. None of K0–K5 has returned a native measurement. There is no measured outliner saving, compatibility verdict or board result. The trial is a single job within Thursday’s existing batch. [0012g review pin and launch instructions](0012g_reply.md)

## Inputs and prerequisites

| Question | Retained evidence | Thursday verification |
|---|---|---|
| Which kernel? | QB 37736448, Official Base 20261113.1. The Product receipt identifies armv7l tztv-kernel-perf 1-1, vdlinux#14293732. The manifest pins shelf 14427407. | Verify the receipt, Product ledger, shelf list, actual P4 overlay and defconfig. Record the installed clang NEVRA from GBS. |
| Which configuration ran? | KANTSU2E_perf_defconfig and an older replay establish relevant source settings. The existing readback did not recover a full effective configuration bound to this QB. | Read a perf config from the verified kernel RPMs or decompress embedded IKCONFIG from the shipped boot image; verify complete ARM settings and reject conflicting copies. Stop before builds if unavailable. Then compare all effective Kconfig keys for K0–K3; require equal K4/K5 Thumb configs and list the delta from K0. |
| Where are the models and how are they selected? | The Official spec supplies the model inputs. ARM and accel libLLVM carry model symbols. The shelved kernel Makefile lines 1065–1070 add both release-advisor options to KBUILD_CFLAGS when their config symbols select them. | Consume the native 9.1/11.1 SRPM spec diff and Official input-object proof. Inspect four groups of real C compilations and capture the LLVM option dump during the build of kernel/sched/core.c. An option dump establishes mode selection; it cannot count individual model decisions. |
| Does K0 reproduce the publication? | Official uImage is 11,348,968 B in both the publication and old replay, with different hashes. Official zImage is 5,326,504 versus 5,326,464 B. The shipped file named vmlinux is 3,696,242 B of detached BTF. | Require the published perf uImage size. A linked QB vmlinux is needed to check its size. Without one, disclose exploratory comparisons separately and return incomplete. An authentic QB linked ELF or build artifact can close this gap. |

[Matched kernel measurements](../../artifacts/evidence/native-run-r0011f-batch-xkHDpd-20261124.txt) · [GBS kernel source and advisor evidence](../../artifacts/evidence/native-run-r0005-20261118.txt) · [Model inputs](../../artifacts/ledger/r0012c-mlgo-inputs.tsv)

## Size and audit table

Each size cell awaits a **new** build. Record raw bytes for linked .text, .rodata, .init.text, total SHF_ALLOC, zImage, uImage and total RPM module file bytes.

| Kernel ISA and advisor mode | As delivered, no added outliner flag | With explicit -moutline | Comparison |
|---|---|---|---|
| A32, both release | K0 · unmeasured | K1 · unmeasured | K1 − K0 |
| A32, both default heuristics | K2 · unmeasured | K3 · unmeasured | K3 − K2 |
| Thumb-2, both release | K4 · unmeasured | K5 · unmeasured | K5 − K4 |

Compute the interaction in bytes as (K1 − K0) − (K3 − K2). Count baseline helpers too. Coexistence requires delivered flags and surviving helpers in the release lane. Module compatibility, unwind coverage and execution on the target are separate tests. Resident .text bytes are a useful first estimate; boot-time reclamation, page boundaries and runtime allocation affect actual RAM.

The trial patch operates inside the staged kernel spec, using one GBS root path, fresh contents and an empty local dependency repository across sequential lanes. K1/K3/K5 append to kernel KCFLAGS. K2/K3 clear the two Makefile advisor overrides for this invocation and require default advisor values on the real TU without editing the A32 .config. A failure to prove the off switch makes the off pair unusable. The Thumb rows select the perf defconfig only. The make wrapper retains a copy of the needed objects and metadata inside the private build tree before packaging cleans them. Patch SHA-256 is `5a3743250a600f0ef3ad019dc1f46834f7e8bb6182557001dafd708e7b0ae92e`. [Trial patch](../../artifacts/patches/kernel/perf-machine-outliner.spec.patch)

| Audit | Result today | Evidence to return |
|---|---|---|
| Actual treatment | No native rows | Effective C argv from kernel/sched, mm, net/core and arch/arm, scheduler TU advisor dump and output config. |
| Outlined helpers | No counts or bytes | Linked helper names, addresses, sizes, direct call sites, input section/object joins and subsystems. An enabled lane with zero surviving helpers fails delivery. Zero alone cannot distinguish a skipped pass from no eligible sequence. |
| Section lifetime | No findings measured | Inspect every restricted-section caller and init-to-resident edge by function. Keep unmatched origins, indirect calls and veneers under review. A linked output section can hide a special input section. |
| Unwind | No measured gaps or coverage | Decode actual ARM EHABI ranges including merged entries, missing ranges and CANTUNWIND. Frame-pointer builds and valid descriptors still require inspection of live unwind behavior. |
| Vendor/external modules | No build or load result | K0/K1/K4/K5 each require the lane's fresh devel RPM header, compiler evidence, modpost without unresolved symbols and expected .ko paths for the installed module owners. Loading remains a board test. |

[Audit implementation](../../artifacts/scripts/r0012f/kernel-audit.py.txt) · [Module checks](../../artifacts/scripts/r0012e/kernel-modules.py.txt)

## Board runbook for K0, K1, K4 and K5

KantSU2E is unavailable this week. Use an approved installable trial image for each kernel and a verified Official rollback USB. The local kernel RPMs alone do not constitute flashable images. Apply each gate on the same board before proceeding.

1. **Identity and recovery.** Match each USB manifest/hash to the intended lane, record the board serial, image build ID, running kernel and installed module RPMs. Use the reviewed BOOST full-image procedure. Verify the kernel image identity and matching symbol artifacts after each flash. Save results as terminal text before switching images. On a wrong identity, boot failure or loss of recovery access, stop and restore the verified Official image using the board runbook. [USB and recovery procedure](0011e_reply.md)
2. **Boot and memory.** Interleave K0/K1 and K4/K5 in matched cycles. For five cold boots per lane, measure the same power-on-to-ready event, wait the same settling interval and record MemFree, MemAvailable, Slab and SReclaimable from /proc/meminfo. Check dmesg for new warnings, faults, unwind and module errors before any deliberate warning. Preserve every run and report median and range. A new fault or an unmeasurable boot boundary precludes acceptance.
3. **Scheduler, memory and loopback.** Five runs each of `perf bench sched messaging`, `perf bench sched pipe`, `perf bench mem memcpy` and the same pinned `hackbench` invocation. For loopback, start `iperf3 -s -1 -B 127.0.0.1` and run `iperf3 -c 127.0.0.1 -t 30`. Use identical tool binaries, workload sizes, governor, affinity, temperature and background service state. Record versions, elapsed time/throughput and failures. Missing tools or throttled runs are visible gaps.
4. **Media.** Play the same SHA-256-identified local 4K asset via the established player, using the same window and playback settings three times. Record player CPU and the start/end value of its validated drop counter, plus free memory. No validated counter or asset means no drop claim.
5. **Unwind and modules on a separate diagnostic boot.** Load only approved matching test/vendor modules. Check SysRq support, console capture, rollback and panic_on_warn policy first. Collect an all-CPU trace using `echo l > /proc/sysrq-trigger` from the authorized board shell. Exercise the reviewed test module’s controlled WARN_ON in the agreed recovery window. Decode PCs with this lane’s vmlinux, load addresses and KASLR offset. Require demonstrable traversal of an outlined helper and its correct caller with no lost or corrupt frame. A trace elsewhere is inconclusive. Keep the intentional warning separate from the clean-boot dmesg. Stop on an unexpected panic, incomplete symbol mapping or unexpected unwind, save the trace and roll back.

Record results in the lane’s board report, including normal-boot logs separately from deliberate WARN output. Board qualification and any production change remain subject to PM review.
