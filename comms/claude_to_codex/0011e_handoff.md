# 0011e — Claude (PM) → Codex: r0011c chain results; Base proof incomplete; board-day runbook

Date: 2026-11-24 (CN).

## Evidence

| File                                                                                                                                      | SHA-256                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `artifacts/evidence/native-run-r0011c-chain-AFkXQV-20261124.txt` (attached; user terminal: progress check plus `combined.txt`, 108 lines) | `35bfa8c9c344417595071f9feefdf01b773efab477a0a10d01a8eb8cf557de16` |
| native `combined.txt`                                                                                                                     | `e535d2ed4605ae603d48bbf42d5a75a6a86965a0fd134fb948b84fb7c95d0dc7` |

All four jobs exited with rc=0, finishing at 16:13:39 CST.

## 1. Results

**GCC reference (`GCC-REF-NOPRELINK`, QB 37564293):**

- `CAPTURE_DIR`: `workspace/qb-evidence/37564293-TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1`, so `GCC_CAPTURE` is set.
- PERF archive: 1,806,199,092 B, `2b8cd7ba…`.
- Published build.conf: `5e78db50…`, with `gcc-warning-build-env` at lines 320/321/425.
- Ledger: 5,880 RPMs.
- Kernel RPMs: 4; `tztv-kernel-perf` is 20,018,029 B.

**USB folders: both ready.**

| Lane       | Folder                              | uImage     | zImage    |
| ---------- | ----------------------------------- | ---------- | --------- |
| Official   | `workspace/usb/37736448/updateSU2E` | 11,348,968 | 5,326,504 |
| Customized | `workspace/usb/37736427/updateSU2E` | 11,085,240 | 5,222,032 |

- **uImage:** both lanes are byte-for-byte the sizes of the 18 Nov GBS replay (Doc 02: 11,348,968 / 11,085,240 B, −2.32%).
- **zImage:** sizes differ from the replay by +40 B (Official) and −272 B (Customized).

Compare the new QB `vmlinux` / kernel sections with the replay. If they are equal, Doc 02's kernel table holds for the matched pair with no re-measurement. Report the comparison as a table.



**MLGO Base proof: `REVIEW_STATUS INCOMPLETE`.** Three gaps:

1. `SRC_METADATA official/custom HTTP Error 404`: the source metadata URL for both Bases is wrong or missing. Find the correct source repo for `tizen-10.0-base-dev-llvm` snapshots 20261113.1 / 20261118.1, or take `llvm-22.1.8-9.1.src.rpm` / `-11.1.src.rpm` from where the OBS project publishes them. Give a command that writes the `MLGO_PROOF_RPMS` TSV.
2. `INSTALLED_REQUIRED … platform image is not ext2/3/4`, so `INSTALLED_NEVRA_DIFFS UNAVAILABLE`. Identify the `platform.img` format (sparse, squashfs, erofs, …) and support it read-only. As a fallback, use the board `rpm -qa` export per lane on board day (your 0010b `sdb` command).
3. Accelerator: `clang-accel-x86_64-armv7l` 0.4-2.4 → 0.4-2.5 come from different SRPMs (`qemu-accel-0.4-2.4` / `-2.5`). In OBS/GBS armv7l builds the x86_64 accel binaries may be the clang that actually executes. State which binary compiled the kernel in each lane, and where the MLGO models are embedded (llvm or accel). This decides whether "Base swap" can be narrowed to "models".

**GCC vs LLVM kernel RPM (for later; do not publish yet):** `tztv-kernel-perf` is 20,018,029 B for GCC, 19,345,448 B for LLVM Official (−3.36%) and 19,160,700 B for LLVM Customized (−4.28%). These images use different Base series and Product snapshots 10 days apart. Before any HQ use, compare the kernel source identity (NEVRA / VCS) of `tztv-kernel` across the GCC and LLVM captures.

## 2. Board day: give one consolidated runbook

The user can flash now. Put these in one reply section, in order, with the new captures filled in:

1. **Copy and verify on the USB stick:** the command that checks `manifest.sha256` against the copied folder on the USB mount.
2. **Step 5 bench staging** (`gbs-board-bench` from 0010 §5) with `OFFICIAL_CAPTURE` = 37736448. The user can start this now, while copying the USB.
3. **Per lane, after flashing:**
   - identity check (`mlgo-tv-identity`);
   - board `rpm -qa` roster export, which feeds the Base proof;
   - the measurement runs (boot ×5, microbench ×5, 4K ×3, memory).

   Alternate the lanes: O, C, O, C… Use the same board and the same procedure.
4. **Readback:** one combined file per lane.

## 3. After board staging

Give the `hq-overnight` start command with `GCC_CAPTURE` and `OFFICIAL_CAPTURE` filled in. It runs tonight and must not overlap Step 5 staging, because both take the shared lock. Use the download retry from 0011d in every `get()`.
