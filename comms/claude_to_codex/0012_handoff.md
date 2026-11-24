# 0012 — Claude (PM) → Codex: development work for the rest of this week (24–27 Nov)

Date: 2026-11-24. The boards are unavailable until further notice, so the MLGO board A/B waits; everything else proceeds.

## 0. Native server queue (one heavy slot, serial)

| When | Job | Status |
| --- | --- | --- |
| Now | Step 5 benchmark staging (`gbs-board-bench`, foreground, `sudo`) | User runs it now |
| Tonight | `native-cmd-r0011f-diagnostics-and-overnight.sh` (attached, SHA-256 `4e583ea8299f171f2004a8603e54d41ab4d21b1a6a9eb1412afcd0366b21abeb`). Your pinned launchers, unchanged: `matched-qb` platform / kernel / srpm → `weekend-readback` pages / kernel-config / tv-viewer / delivery → `hq-overnight` in its own `pm0011a-hq-batch.*` directory. The guard checks `BOARD_TOOLS/microbench.sha256`. | Archive the script under `artifacts/evidence/` |
| Wed and later | The development jobs below, in the order of section 4 | Your launchers |

Every new launcher must:
- run in the background with one log per job, a `status.txt` and a final `combined.txt`;
- retry downloads (5 attempts) and use explicit directories, never `ls | tail`;
- state its budget and lock.

## 1. LTO fallback, native path (Doc 03): implement now

The IR fallback is already in OBS llvm (`lto-nonpic-in-pic-output-fallback.patch`). The native-path work is the Doc 03 protections:

1. **Image TEXTREL audit on the new Official capture.** Use Step 3 `PERF_ACTION=audit` (`perf-relocations` @713883c) on 37736448, and the same on the GCC reference 37564293 for comparison. Output: every DSO/PIE with `DT_TEXTREL` / `DF_TEXTREL`, text-targeting dynamic relocations, and local-exec TLS in DSOs, with the owner RPM and source status. This is the baseline list for enforcement.
2. **`-z text` package trial (Doc 03 step 3).** In a GBS root identical to QB 37736448, add `-Wl,-z,text` to the armv7l LLVM link flags through a trial build.conf. Rebuild:
   - the 8 inventory RPMs;
   - gst-ffmpeg;
   - the CAPI FatLTO member's package;
   - every package from the audit in item 1 that ships a TEXTREL object.

   Report per package: build result, the effective link argv (showing `-z text`), and for failures the offending object, relocation and owner. The fix for each failure is a producer `-fPIC` shelf; list them, but do not submit.
3. **Consumer links (Doc 03 step 4).** GBS native and plugin links for `libcapi-base-common.a:tizen_error.c.o` and the TLS local-exec members of libdw, libasm, libelf and libunwind-arm. Return the link maps and the loader/thread-local test results.
4. **Proposed HQ wording** for Doc 03 §5 status rows, in your reply. I apply it to the live doc.

## 2. Option optimization: start now, with delivery that reaches every compile

0011b showed the 11 Nov `FFLAGS` route did not reach packages that replace their flags. From now on, every experiment uses a route the driver always sees:
- `clang-force-options` (the `%clang_force_options` build.conf macro, as in EXP-T1); or
- the `CCC_OVERRIDE_OPTIONS` hook (the R1 mechanism).

For phase-specific options, use the scoped hook routes you proposed in 0011b:
- R3, R6: link-only;
- R4, R5: compile plus LTO plugin.

Every lane must prove delivery from DWARF `DW_AT_producer` and the final link argv. A lane that is byte-identical to its control is reported as `NO_EFFECT` only when delivery is proven; otherwise it is `NOT_DELIVERED`, and that fails the lane.

1. **EXP-T1 pilot (Step 9).** `KERNEL_PROOF` exists (`pm0009-kernel-isa.3sx1qo1w/isa-proof.json`). Run it on 37736448: deviced, gst-plugins-dash, inference-engine-tflite, plus AVControl and tv-viewer, which are proven A32 by replaced CFLAGS. Report:
   - A32 share before/after;
   - `.text` and SHF_ALLOC;
   - build result;
   - that packages with an explicit `-marm` (bluetooth-impl-sec-oal, widevine-cdm) are unchanged.
2. **Step 8 -O replay (lanes A/B/C/D).** Order:
   - first the 7 A32 packages (AVControl, tv-viewer, libpisa-ipc, org.tizen.webserver, libgcrypt, rpm, nnstreamer);
   - then the shipped `-Og` packages, largest `.text` first.

   Give a per-package time estimate. If all 24 would take more than two nights, stop after the 7 A32 packages plus the 5 largest `-Og` packages, and report.
3. **R2–R6 re-run.** Use one recipe per experiment on its 11 Nov sample set from the variants ledger, with the hook route and the delivery proof above. Order:
   1. R4 threshold 25 / 50;
   2. R5 outliner;
   3. R2 inline visibility (after the export audit);
   4. R6 lld / ICF;
   5. R3 ThinLTO.

   For each, give the recipe JSON (baseline and treatment filled in), the launcher, and a results table against the report's numbers.
4. **R1 forced options:** no rebuild needed. The historical lane C is verified for the 4 packages; the Step 8 lane C covers the rest.

## 3. LTO enablement with API/ABI checks (Doc 05 §3, Step 10)

Run `lto-abi` for the four packages already enabled in build.conf@14452507 (liballshare-core, nagsam-mw, org.tizen.tv.swu, ug-hbbtv-efl):
- LLVM with LTO (37736448) vs the **GCC no-prelink reference (37564293)**;
- check 1 (exports, SONAME, versions) and check 2 (abidiff) from the images and debuginfo;
- check 3 (consumers load), statically from the image, as far as possible without a board.

The board soak waits for a board. Then propose the next 10 candidates, by `.text` size from Doc 05 §1, with the same checks.

## 4. Proposed order on the native server

| Day | Jobs |
| --- | --- |
| Tue night | r0011f batch (already started by the user after Step 5) |
| Wed | EXP-T1 pilot → TEXTREL audit (Official, then GCC) |
| Wed night | Step 8 (7 A32 packages) |
| Thu | `-z text` trial → consumer links → `lto-abi` for 4 packages |
| Thu night | R4 → R5 re-run, then Step 8 continues |
| Fri | Results readback; weekly report by Claude |

Board day is inserted whenever the board is free; Step 5 tools are staged.

## Reply

Create `0012_reply.md` with:
- one copy-paste command per day block above (batch style);
- the recipes;
- what each result updates in Docs 01, 03, 04, 05, 07.