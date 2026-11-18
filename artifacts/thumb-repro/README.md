# Thumb reproduction

[Verified] Local re-decoding of retained ELF metadata reproduced the labelled 17 November scan on the then-installed board. The scan examined 5,120 unpacked ARM ELF paths from /usr, /prd and /opt with recorded exclusions. It counts byte spans between Arm ELF mapping symbols `$a`, `$t`, `$d` within executable sections. Classify a file only when one mode exceeds the other mode plus unknown executable bytes. Data spans are excluded from that comparison. [Arm ELF specification](https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst)

- [Reproduced 27-file ARM list](retained-board-arm-baseline.csv) includes Build IDs and the seven matched DWARF records with `-marm` evidence.
- [Counts and unknown breakdown](reproduction-summary.txt) reproduce 27 ARM, 232 Thumb and 4,861 unknown. All unknowns have no usable A/T span. Across the inventory, 4,860 files lack a static symbol table. Missing mapping symbols in stripped ELF dominate the result.
- [Debug review](../evidence/thumb-debug-review.txt) preserves source examples and pending compile commands.

The historical 106 figure has no recoverable input list, image identity, threshold or file scope in the reviewed records. D-019 requires reproducing it before claim reuse. Use this labelled retained baseline and match more debuginfo by Build ID on the current image. Check actual compiler commands and source directives before assigning cause. Estimate gains by paired ARM/Thumb recompiles of the affected objects with other flags fixed. No per-file size gain can be inferred from mapping spans alone.
