# PM → Codex, round 0008: LTO fallback native path (HQ due TODAY) + user answers

## A. User answers (record them in DECISIONS/STATUS)

1. **"ASAN" is only the QB job name.** The PERF image is not AddressSanitizer-instrumented. The user stated this. Close the gate on that basis.
   - When the Customized capture lands, add a cheap confirmation to an existing readback: no `__asan_` symbols and no `libasan` NEEDED in about 10 sampled PERF ELFs.
   - Do not block the rebuild on it.
2. **Product sources.** Product (GCC) sources cannot be changed; only the LLVM side can. Both LLVM QBs build from the same Product sources. QB has no Product changelist pin to set.
   - So the matched pair is made by **starting both QBs at the same time with identical inputs**, only the Base URL differing.
   - The 9-package `.text` delta in the old pair is explained by the two QBs running on different days. The 9-source join (command 3) still documents it.
   - Update D-038 and the report wording.

## B. HQ deliverable due today: LTO fallback "native path" design. My review of `hq/PIC_FatLTO_Dual_Path_Design.md`

To HQ we wrote: *"We are evaluating protection for both consumption paths… We will provide the proposed design, coverage boundaries and verification plan by Friday."* (`artifacts/evidence/hq-fat-lto-draft.txt`).

The current file has good technical content, but it is not yet the deliverable. It reads as an evidence log. **The decisive gap: it does not close the native path's silent-failure case.**

1. **Silent native case: TEXTREL.**
   - The 56-case matrix rejected the 18 native cases only because it linked with **strict `-z text`**. Production link flags (`-Wl,-z,relro,--as-needed …`) carry no `-z text`.
   - With GNU ld, a non-PIC `R_ARM_ABS32` (and similar) in a shared object or PIE does not fail the link. It produces dynamic relocations against text plus `DT_TEXTREL`.
     - At best, text pages become private-dirty, which costs memory on a 1 GB target.
     - At worst it fails at runtime. Our own history has one: `libgstomx.so` failed with `unexpected reloc type 0x03` (`artifacts/historical-reports/stability-report.md` L46). That is exactly the native-path failure HQ is worried about.
   - MOVW/MOVT ABS and `TLS_LE32` in `-shared` do fail at link time. ABS32 does not.
   - **Verify each of these claims on the GBS root:** a non-PIC ABS32 object, linked `-shared` without `-z text`, yields `TEXTREL` and links successfully.
2. **The design must give, per path: protection, coverage boundary, verification.** Proposed structure (one to two pages, HQ-readable, no progress narrative):
   - **IR path** (plugin claims bitcode):
     - Protection: the existing regular-LTO non-PIC fallback plus its tagged diagnostic.
     - Boundary: regular LTO only. State ThinLTO and GCC LTO behaviour.
   - **Native path** (the fat object's native code, or non-LTO objects, consumed by GNU ld/GCC/no-LTO links). Protection is defense in depth:
     - (a) **Prevent at producer.** Build `-fPIC` for every object shipped in `*-devel(-static)` packages or consumed by a DSO/PIE. Only LLVM-side shelves are allowed (user rule), so state that the policy is applied through LLVM migration shelves, as with the existing PIC-fix shelves.
     - (b) **Fail at link.** Add `-Wl,-z,text` to the LLVM build.conf link flags for armv7l. This turns silent TEXTREL into a build error, so a non-PIC native consumption cannot ship. Allow a narrowly documented exemption list.
     - (c) **Gate per image.** An automated scan of every shipped DSO/PIE: `DT_TEXTREL`, text-targeting dynamic relocations (`R_ARM_ABS32`/`REL32` in executable segments), and `TLS_LE` in DSOs. This formalises the existing manual "library scan (TEXTREL / REL32)" from the stability report into a release gate.
     - (d) **Prebuilt and vendor inputs.** Obtain a PIC variant or reject the consumer. No machine-code rewriting, and say plainly why.
   - **Coverage boundary table:** covered, detected, and out of scope. Examples:
     - covered: absolute data relocations, code relocations, local-exec TLS in DSOs;
     - out of scope: semantic ABI mismatches such as the Bluetooth case, and non-PIE fixed-address executables by design.
   - **Verification plan with owners and order:**
     1. the 56-case matrix rerun **without** `-z text`, to show what (b) and (c) catch;
     2. the `-z text` build.conf trial on the 9 acceptance entries plus the capi-base-common FatLTO member;
     3. the TEXTREL/REL32 gate run on the current image (Customized capture, then the matched rebuild);
     4. the GBS `MODE=pic` consumer links (still never run).

     Each step gets a pass criterion. No dates you cannot hold.
3. **Before anything goes to HQ:**
   - Check whether `-z text` would break anything known today. Run the TEXTREL scan first. If shipped DSOs already have TEXTREL, list them; they are both the exemption list and the work list.
   - The image ELF ledger may already record `DT_TEXTREL`. If it does, report the count now from retained data, with no new native run.

## C. Deliverables, today, in this order

1. A TEXTREL/REL32/TLS_LE scan launcher that runs on retained data, or on the Customized capture if retained data lacks it. Light, no heavy lock if possible. I will review it and give it to the user.
2. A native GBS check that ABS32 without `-z text` links with TEXTREL (one tiny fixture inside the existing GBS root; seconds). Fold it into the scan launcher if that is simpler.
3. `hq/PIC_FatLTO_Dual_Path_Design.md` rewritten to the structure in B.2, HQ-ready. Numbers only from verified evidence; no "pending/need to check" wording. Put open items in the verification plan as planned steps with pass criteria.
4. Confirm or refute B.1 with evidence. If production already uses `-z text` somewhere I missed, say where.