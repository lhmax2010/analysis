# ARM32 static PIC audit

- [Screening code](arm-pic-audit.py.txt) interprets ELF sections and GNU/BSD archive members. The relocation target comes from the relocation section `sh_info`. Only executable targets are screened. The file preserves marker evidence for LLVM and GCC LTO, relocations, member ordinals and digests.
- [Native runner](native-audit.py.txt) verifies fixture input hashes and streams repository RPM contents without extracting member paths. It records each RPM status and each selected file or member.
- [56 original cases and fixture identities](tizen-arm-fixture-index.csv) and the [92 pinned RPM identities](rpm-identities.csv) are native inputs.
- [Local classifier smoke](local-classifier-smoke.csv) exercises a true ARM object and archive path. The flagged input has three executable absolute relocations. A control fixture carries REL32 in code and ABS32 in debug data, demonstrating section scoping.

[Verified] The original Tizen matrix recorded 18 native relocation rejections and 38 link/runtime passes. Local smoke used small ARM assembler objects and a cross-check with GNU readelf. Retained Tizen object bytes are on the native server. Check all 56 case rows against their SHA-256 and require the classifier to flag the 18 rejections and no PIC positive fixture before screening production RPMs. If fixtures were removed, establish their status from the retained workspace before recreating them.

The screen recognizes the listed absolute and TLS local-exec relocation types. It reports evidence and review status. A flag can be appropriate for a CRT, kernel or fixed-address consumer. Proposed allowlists require artifact scope, intended consumer and a reason. Keep unrecognized formats, thin archives and missing payload paths visible. Preserve GNU LTO markers independently from `.llvm.lto`. [Arm ELF relocation definitions](https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst)

[Verified metadata] The first shipment screen includes 43 Product and 49 Base identities with direct static paths. Build-tree-only inputs, nested containers and extensionless candidates still need their own scan. File metadata alone gives no measured defect count. Full commands are in [reply 0002](../../comms/codex_to_claude/0002_reply.md).
