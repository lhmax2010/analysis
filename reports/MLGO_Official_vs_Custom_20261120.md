# Official versus Customized MLGO — kernel comparison record

This draft records the planned KantSU2E comparison for Friday, 20 November. Run-level results and a conclusion are pending.

The 11 November image report recorded release MLGO in the Linux kernel and byte-identical outputs in the sampled user-space control after disabling ML inlining. For this image pair the kernel is the primary measurement and user space is the identity control. The current board boots Linux 6.12.60 built by Clang/LLD 22.1.8, with tztv-kernel-perf installed. The planned shelf list selects the vdlinux change that records both advisor switches. The post-login source gate passed. Actual QB argv and compiler-install records remain unavailable through the current REST account. Use the source and image criteria below to interpret the Base comparison. [Kernel evidence](../artifacts/evidence/kernel-mlgo-source-chain-20261117.txt)

| Lane | Inputs to record |
|---|---|
| Official | Base 20261113.1, current KantSU2E image, QB 37627297 control configuration, kernel image checksum, package and compiler identity |
| Customized | Base 20261118.1, pinned LLVM rev12 on armv7l/x86_64, matching Product/build.conf/shelves, candidate QB ID, package and compiler identity |

The operator already started the candidate QuickBuild with Base 20261118.1 and the other QB 37627297 inputs. Its job ID, completion and Product URL are pending. The kernel gate determines the label and conclusions. The wider same-rev12 reference/custom rebuild and global advisor options are deferred.

| Metric | Procedure | Result |
|---|---|---|
| Kernel and modules | Same perf variant; compare Image, published zImage/uImage where present, vmlinux section bytes and installed .ko counts/sizes. Separate stripped/unstripped and compressed/uncompressed sizes. | Pending |
| Boot | Five matched cold boots per lane; same board, firmware and Home-ready marker | Pending |
| Kernel microbenchmarks | Preselect runnable syscall, scheduling/context-switch and memory probes; five blocked runs per lane after a warm-up, fixed CPU affinity, frequency policy and load | Pending |
| Normal-memory 4K | Three matched runs per lane; identical stream/player/firmware, CPU and dropped or late frames, stalls and new regression signatures | Pending |
| User-space identity | SHA-256 by installed path and package owner on identical scope; list added, removed and byte-different ELF, with Build IDs for triage. Correlate with non-LLVM inventory delta and rebuilt package records. Treat every unexplained difference as a confounder. | Pending |

Keep each run and both exact artifacts. Preserve rollback before flashing. Report median, IQR, interval and all absolute regression events. Capture compiler/version, model evidence and any kernel source/config/link-mode difference alongside the result. User-space identity concerns file bytes. It does not imply equal runtime behavior after a kernel change.

## Model identity before reporting

Independently prepare vdlinux baseline 14293732 with shelf 14427407 and the KantSU2E perf defconfig. Compare both Base compilers in four advisor modes using three fixed kernel translation units and the probe. Keep differing default artifacts or identical release artifacts as findings. Retain the effective QuickBuild compiler as unverified until its package build evidence arrives. [Standalone model identity launcher](../comms/codex_to_claude/0004_reply.md#g-standalone-mlgo-model-identity-replay-for-friday)

The 2,342-RPM image comparison is staged for the candidate Product URL. Board measurement tools and the attended flash/rollback checklist are ready for review. Exact approved flash/recovery instructions and a verified playback drop counter are still needed for live runs. [Image and board procedures](../comms/codex_to_claude/0004_reply.md#h-official-versus-customized-product-payloads)

## Round 0005 preflight and confounders

Native preflight shows identical Base and shelf lists and 3,000 delta rows, 2,952 outside LLVM. The previous successful OBS status packet records rev12 published/succeeded on both arches. The read-only direct Python transport will verify actual RPM bytes after the initial OSC proxy error. The image comparison uses the same retained non-LLVM input as the installed-overlap and release/version classification. Candidate job ID and Product URL, installed overlap, and observed image and TV results remain pending. [Round 0005](../comms/codex_to_claude/0005_reply.md)


## Source gate and image attribution

**Source-level gate passed.** The pending vdlinux shelf 14427407 selects Base Clang and LLVM under `_toolchain clang`, sets `LLVM=1 LLVM_IAS=1`, and enables `CONFIG_MLGO=y` in the KantSU2E perf defconfig. The Kconfig and shelf description identify both release advisors. Read the corrected Makefile excerpt for direct line-level corroboration. The QuickBuild kernel log remains unavailable after REST HTTP 403. Effective argv and the exact executing compiler remain unverified. [Round 0005 addendum](../comms/codex_to_claude/0005_reply.md#addendum-a--kernel-source-gate-passed)

**Image attribution is pending.** If `tztv-kernel-perf` differs between the two images and every covered user-space ELF outside the item 2 Base-delta packages is byte-identical, report the observed difference as a kernel-focused Base-swap result supported by the source gate and the image comparison. List all user-space differences within the Base delta, flag affected benchmark dependencies, and record any unresolved or unexplained ELF as a confounder. This scope supports a Base-swap association. Production advisor execution and model-only effects require their own evidence.
