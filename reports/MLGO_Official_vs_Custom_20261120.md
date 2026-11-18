# Official versus Customized MLGO — kernel comparison record

This draft records the planned KantSU2E comparison for Friday, 20 November. Run-level results and a conclusion are pending.

The 11 November image report recorded release MLGO in the Linux kernel and byte-identical outputs in the sampled user-space control after disabling ML inlining. For this image pair the kernel is the primary measurement and user space is the identity control. The current board boots Linux 6.12.60 built by Clang/LLD 22.1.8, with tztv-kernel-perf installed. The planned shelf list selects the vdlinux change that records both advisor switches. Confirm source rules or actual kernel compiler commands and the Base compiler installed by each QB job. A cached, reused, prebuilt, or heuristics-only kernel does not establish an Official versus Customized model comparison. [Kernel evidence](../artifacts/evidence/kernel-mlgo-source-chain-20261117.txt)

| Lane | Inputs to record |
|---|---|
| Official | Base 20261113.1, current KantSU2E image, QB 37627297 control configuration, kernel image checksum, package and compiler identity |
| Customized | Base 20261118.1, pinned LLVM rev12 on armv7l/x86_64, matching Product/build.conf/shelves, candidate QB ID, package and compiler identity |

The operator submits the candidate after the preflight verifies the two PINNED_LLVM_BINARY results and the intended Base-list diff. The kernel gate determines the label and conclusions. The wider same-rev12 reference/custom rebuild and global advisor options are deferred.

| Metric | Procedure | Result |
|---|---|---|
| Kernel and modules | Same perf variant; compare Image, published zImage/uImage where present, vmlinux section bytes and installed .ko counts/sizes. Separate stripped/unstripped and compressed/uncompressed sizes. | Pending |
| Boot | Five matched cold boots per lane; same board, firmware and Home-ready marker | Pending |
| Kernel microbenchmarks | Preselect runnable syscall, scheduling/context-switch and memory probes; five blocked runs per lane after a warm-up, fixed CPU affinity, frequency policy and load | Pending |
| Normal-memory 4K | Three matched runs per lane; identical stream/player/firmware, CPU and dropped or late frames, stalls and new regression signatures | Pending |
| User-space identity | SHA-256 by installed path and package owner on identical scope; list added, removed and byte-different ELF, with Build IDs for triage. Correlate with non-LLVM inventory delta and rebuilt package records. Treat every unexplained difference as a confounder. | Pending |

Keep each run and both exact artifacts. Preserve rollback before flashing. Report median, IQR, interval and all absolute regression events. Capture compiler/version, model evidence and any kernel source/config/link-mode difference alongside the result. User-space identity concerns file bytes. It does not imply equal runtime behavior after a kernel change.

## Model identity before reporting

Compare both Base compilers in the four advisor modes using the selected pinned kernel translation units and the probe. Record the actual kernel job host compiler match, both Customized snapshot RPM pins, per-mode object hashes and optimization remarks. Keep differing default artifacts or identical release artifacts as measured findings. Native results are pending. [Round 0004 model identity launcher](../comms/codex_to_claude/0004_reply.md#g-mlgo-model-identity-replay-for-friday)
