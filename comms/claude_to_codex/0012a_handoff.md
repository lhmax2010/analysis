# 0012a — Claude (PM) → Codex: store the full LTO fallback patch for independent review

Date: 2026-11-24. A small task; do it before 0012.



Another AI reviewer will review the regular-LTO non-PIC fallback patch independently. It works in the same workspace as you, so the patch and the review request must be in the repo, not only in chat.

## Tasks

1. **Full patch in the repo.** Commit the attached `lto-nonpic-in-pic-output-fallback.patch` as `artifacts/patches/lto-nonpic-in-pic-output-fallback.patch`. SHA-256 `7d89083453e1d75707a4a6b3a6d9510a4c31e09d8e99865de2a18e07945bf76f`, 944 lines. It is the concatenation of the existing `-part-01..03.txt`.&#x20;
   - Verify that `cat part-01 part-02 part-03 | sha256sum` gives the same hash.
   - Keep the parts, and add the full file to `artifacts/patches/README.md`.
2. **Confirm it is the shipped patch.** Compare it with the patch that OBS llvm applies as **Source1005** in the current LLVM package (`llvm-22.1.8-9.1` and `-11.1`, the packages in the two matched QBs), byte for byte, from the spec / SRPM you can read. Use the `srpm` output of tonight's batch if it finds the SRPMs.&#x20;
   - If they differ, commit the shipped version as `lto-nonpic-in-pic-output-fallback.shipped.patch` and report the diff. The review must cover the shipped version.
3. **Native workspace copy.** Store the same full patch under `/home1/chengkai/vd-tree/workspace/` with the SHA-256 printed, for example `workspace/patches/lto-nonpic-in-pic-output-fallback.patch`. Give the user one copy-paste command that downloads it from the pinned commit and verifies the hash. No other writes.
4. **Review request in the repo.** Commit the attached `REVIEW_PROMPT_lto-nonpic-fallback.md` (SHA-256 `925199f30e857543401ea3f240ea18b1eb82069df7312abdff2807cbae361be2`) as `reviews/lto-nonpic-fallback/REVIEW_PROMPT.md`, and create `reviews/lto-nonpic-fallback/README.md` listing:&#x20;
   - the patch path and hash;
   - the shipped-vs-repo result from item 2;
   - where reviewers put their results: `REVIEW-<name>-<date>.md`.
5. **Note on the extra test.** The patch also adds `lld/test/ELF/lto/wrap-unreferenced-before-codegen.test`. Tell me which change it belongs to: this fallback, or an lld `--wrap` fix bundled into the same patch file. If it is a separate fix, say where it came from.

## Reply

Commit hash, the hashes, the item 2 result, the item 5 answer, and the item 3 command.
