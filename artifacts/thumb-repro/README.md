# Thumb reproduction

[Verified] Local re-decoding of retained ELF metadata reproduced the labelled 17 November scan on the then-installed board. The scan examined 5,120 unpacked ARM ELF paths from /usr, /prd and /opt with recorded exclusions. It counts byte spans between Arm ELF mapping symbols `$a`, `$t`, `$d` within executable sections. Classify a file only when one mode exceeds the other mode plus unknown executable bytes. Data spans are excluded from that comparison. [Arm ELF specification](https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst)

- [Reproduced 27-file ARM list](retained-board-arm-baseline.csv) includes Build IDs and the seven matched DWARF records with `-marm` evidence.
- [Counts and unknown breakdown](reproduction-summary.txt) reproduce 27 ARM, 232 Thumb and 4,861 unknown. All unknowns have no usable A/T span. Across the inventory, 4,860 files lack a static symbol table. Missing mapping symbols in stripped ELF dominate the result.
- [Debug review](../evidence/thumb-debug-review.txt) preserves source examples and pending compile commands.

The historical 106 figure has no recoverable input list, image identity, threshold or file scope in the reviewed records. D-019 requires reproducing it before claim reuse. Use this labelled retained baseline and match more debuginfo by Build ID on the current image. Check actual compiler commands and source directives before assigning cause. Estimate gains by paired ARM/Thumb recompiles of the affected objects with other flags fixed. No per-file size gain can be inferred from mapping spans alone.

## Round 0003 mode coverage

The retained `.dynsym` byte scan now covers all 5,120 rows. It yields 185 additional ARM and 1,658 additional Thumb lower-bound classifications, with 3,018 still unresolved. The strict threshold requires known mode bytes to exceed opposite plus all unknown executable bytes. Preserve the earlier mapping-only 27/232 counts as a separate method. Alias intervals are unioned and conflicts remain unknown. [Weighted coverage and per-file CSV](mode-coverage/README.md)

The retained debuginfo summary reports unknown mapping spans. It did not establish that each debug file lacks `.symtab`. Verify the actual retained file with Build ID, section headers and exact mapping symbol names. Then associate debug symbol sections with the runtime virtual addresses before merging. The paired size queue starts with bluetooth-impl-sec-oal and widevine-cdm once their source and ARM-only files are identified. Bluetooth audio and DRM playback are required before accepting changes.

Round 0004 supersedes the dynsym cohort for HQ follow-up. The user is running the full installed-RPM scan. Preserve both method labels for traceability. The 0003 HQ appendix was withdrawn and was never sent. See [106 provenance](origin-106.md) and [the new draft](../../hq/HQ_ARM_Mode_Reply_DRAFT_20261117.md).
