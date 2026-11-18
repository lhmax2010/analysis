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

The standalone replay started in `pm0004-kernel-src.gzu4jw62`. The operator reports it is at the Perforce print stage. No compiler or comparison results have returned. [Native run](../artifacts/evidence/native-run-r0005-20261118.txt#L224)

The 2,342-RPM image comparison is staged for the candidate Product URL. The KantSU2E checklist records the operator's BOOST sequence, separate menu and write gates, Official rollback verification and the three measurement protocols. The Official download awaits a native run. The candidate bundle, image fingerprint mapping, flash completion prompts and playback drop source remain pending. [Board-day procedure](KantSU2E_MLGO_Board_Day_0005.md)

## Round 0005 preflight and confounders

Native preflight verified identical Base and shelf lists and counted 3,000 delta rows, 2,952 outside LLVM. The direct OBS replay proved the following published Base 20261118.1 Clang RPM bytes correspond to OBS revision 12, source digest `0b38aead137ec42dcd99dee28091acc1`. The hashes identify the published RPMs. The kernel compile command and resolved executable remain open. [Native binary pin](../artifacts/evidence/native-run-r0005-20261118.txt#L3)

| Architecture | Published Clang RPM | SHA-256 |
|---|---|---|
| armv7l | `clang-22.1.8-11.1.armv7l.rpm` | `6e692d5fb4f372c9e8d8f969b5171ce73275a7f613ae1f9694797758cf66b1a9` |
| x86_64 | `clang-22.1.8-11.1.x86_64.rpm` | `ed6db88c182662fb81007ffe4589c49792970e14d110b95ebf6744de2949a3d2` |

| Non-LLVM category | Classified events | Unique name/arch | Board name/arch | Board exact Official NEVRA |
|---|---:|---:|---:|---:|
| Release only | 1,363 | 1,354 | 175 | 174 |
| Ambiguous multi-version | 52 | 26 | 2 | 2 |
| Same NEVRA with payload difference | 18 | 9 | 1 | 1 |
| Version or epoch change | 0 | 0 | 0 | 0 |

The deduplicated name/arch overlap is **177 of 2,342**. Category counts overlap. Zero version changes describes the resolved version/epoch pairs. The 52 ambiguous events still require reconciliation. This is a repository-to-installed-inventory join. Compare actual image payloads, including the same-NEVRA case and workload-relevant release bumps, before attributing observed differences. Candidate job ID, Product URL and image/TV results remain pending. [Native Base delta](../artifacts/evidence/native-run-r0005-20261118.txt#L11)

## Source gate and image attribution

**Source-level gate passed.** The pending vdlinux shelf 14427407 selects Base Clang and LLVM under `_toolchain clang`, sets `LLVM=1 LLVM_IAS=1`, and enables `CONFIG_MLGO=y` in the KantSU2E perf defconfig. Makefile lines 1065–1070 add `-mllvm -enable-ml-inliner=release` and `-mllvm -regalloc-enable-advisor=release` to `KBUILD_CFLAGS` under `CONFIG_MLGO_INLINER` and `CONFIG_MLGO_REGALLOC`, respectively. The QuickBuild kernel log remains unavailable after REST HTTP 403. Effective argv and the exact executing compiler remain unverified. [Native source gate](../artifacts/evidence/native-run-r0005-20261118.txt#L22)

**Image attribution is pending.** If `tztv-kernel-perf` differs between the two images and every covered user-space ELF outside the item 2 Base-delta packages is byte-identical, report the observed difference as a kernel-focused Base-swap result supported by the source gate and the image comparison. List all user-space differences within the Base delta, flag affected benchmark dependencies, and record any unresolved or unexplained ELF as a confounder. This scope supports a Base-swap association. Production advisor execution and model-only effects require their own evidence.

Reconcile candidate-only and removed packages against the actual board inventories. Verify workload-relevant non-ELF inputs and dependencies even when changed packages are in the expected Base delta. The four-mode replay diagnoses selected translation units. Require production compiler and linker provenance and the actual LTO path before correlating its observations with kernel Image differences. [Round 0005 independent review](KantSU2E_MLGO_Board_Day_0005.md#independent-review-of-mlgo-attribution)
