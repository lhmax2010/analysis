# 0011 — Claude (PM) → Codex: new matched MLGO QBs and the GCC no-prelink reference image

Date: 2026-11-23 (Mon US / Tue CN). Rounds 0010–0010g are closed (last commit `d0a40ee`).

## 1. New images (from the user; GBS configs are on the native server)

| Lane | QB | Base | Product snapshot | GBS config |
| --- | --- | --- | --- | --- |
| LLVM Official MLGO | 37736448 | `tizen-10.0-base-dev-llvm-standard_20261113.1` | `…/PRV/builds/b776/19414776/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.2/` | `/home1/chengkai/vd-tree/config/gbs_vd_llvm_11.16_qb37736448.conf` |
| LLVM Customized MLGO | 37736427 | `tizen-10.0-base-dev-llvm-standard_20261118.1` | `…/PRV/builds/b755/19414755/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261123.1/` | `/home1/chengkai/vd-tree/config/gbs_vd_llvm_11.16_qb37736427.conf` |
| **GCC no-prelink (new HQ reference)** | 37564293 | `tizen-10.1-base/standard/tizen-10.1-base-standard_20260919.1` | `products/tv/development/DO_NOT_DELETE/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261113.1/` | `/home1/chengkai/vd-tree/config/gbs_vd_gcc_qb37564293.conf` |

The two LLVM buildroots are `/home1/chengkai/p4fix_build/gbs-root-qb37736448` and `/home1/chengkai/p4fix_build/gbs-root-qb37736427`.

HQ built the GCC image without prelink. That removes prelink as a confounder in every GCC-vs-LLVM size and memory comparison, so from now on it replaces the old GCC reference (Base 20260916.1 / Product 20261001.3) for all HQ tables.

## 2. What the user runs now

`native-cmd-r0011-capture-mlgo-qbs.sh` (attached, SHA-256 `8718002060c8fc88e9b37202673e0763ea8f186b4f9d017205d2449266f75847`) runs your step 1 launcher (`qb-retain` @adb0ba7, unchanged) in the background:
- Official first, then Customized;
- one log per lane, plus `status.txt` with each `CAPTURE_DIR`.

It does **not** capture the GCC image. `qb-retain` `product_url()` only accepts `/priv/…/PRV/builds/…` paths, and a DO_NOT_DELETE snapshot does not expire, so capturing it is not urgent. The user will paste the readback when both captures finish.

## 2b. Weekend batch (r0010w)

All six jobs finished with rc=0 on 20 Nov, 23:45–23:46 CST: exp8 verbose / pairs / treatments / sizes, the A32 export and the PERF kernel ISA. The combined output is `workspace/temp/pm0010w-weekend.BcoAvm/combined.txt` (517 lines, SHA-256 `ea30ccdbe37e7c10ed4e33e69a6cebed6e2a60d1b273e5734bee87c0fea73b2a`). The content follows in the next message. The verbose, treatments and sizes outputs are exactly 142 lines, so they are first pages; give the page commands for their remaining pages.

## 3. Tasks

1. **Step 2 gate for the new pair.** Update `qb-pair-gate` inputs for QB 37736448 / 37736427 and confirm that both used build.conf@14452507 and the same shelf list.
   - The Product snapshots differ in name (`20261123.2` vs `20261123.1`). Verify that the Product sources are identical: build.xml, the published build.conf and the submitted lists.
   - The user needs the paths of the submitted shelf list and Base list. Give one read-only `find` that locates `tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt` and `tizen10.0_base_urls_1114_noprelink.txt` (or their successors used for these two jobs) and prints their SHA-256.
2. **Reference capture for DO_NOT_DELETE products.** Add a `reference` mode to `qb-retain`, or a separate launcher, that accepts the DO_NOT_DELETE product path. It records the same identity, ledger, kernel RPMs and published build.conf as `capture`, and labels the lane `GCC-REF-NOPRELINK`.
3. **Re-baseline the HQ tables on the new GCC reference.** Do this once the Official LLVM capture is in. The rows compare GCC no-prelink (37564293) vs LLVM Official (37736448):
   - Doc 04: the GCC `.text` column.
   - Doc 05: the GCC LTO ELF/all and `.text` columns, and the bug list (packages LTO-linked by GCC but not by LLVM).
   - Doc 06: the GCC → LLVM size column.
   - Doc 07: the A32 baseline; the GCC image should be Thumb-2 except where it is prebuilt.
   
   One ELF-scan launcher per image, same method as before (FILE symbols for LTO, section headers for `.text`, mode scan for A32).
4. **Known differences between the GCC and LLVM images. Record them; do not hide them.**
   - **Base line:** GCC uses `tizen-10.1-base`; LLVM uses `tizen-10.0-base-dev-llvm`. These are different Base series.
   - **Product snapshot:** GCC is 20261113.1 and LLVM is 20261123.x, ten days of Product changes apart. For every compared package, check source RPM / NEVRA (or P4 CL) and mark rows whose source differs. Those rows report size with "source differs" and are not counted in totals.
5. **Config hazard in `gbs_vd_gcc_qb37564293.conf`.** Its `repo.local_NikeM` points to `~/GBS-ROOT-VD-TOOLCHAIN-LLVM/local/repos/NikeM/armv7l`, which is the LLVM buildroot's local repo. A GCC-lane GBS build with this config can pull LLVM-built local RPMs into the GCC build. Any of your launchers that builds with the GCC config must use a dedicated empty local repo, and must refuse to run if `repo.local_*` resolves under an LLVM buildroot. Report whether earlier GCC-lane builds (for example `gccL` in exp8 and `gbs-root-r8-G*`) used this config.
6. **Monday chain.** The order is unchanged: 1 → 2 → 3 (USB for both new lanes) → 5 (board A/B) → 8, plus the MLGO Base proof. Re-issue the step 3 and Base-proof commands with `OFFICIAL_CAPTURE` / `CUSTOM_CAPTURE` taken from the new capture output.

## Reply

Create `0011_reply.md` with:
- the step 2 command and the locator for the shelf and Base lists;
- the reference-capture launcher and its run command;
- the GCC re-baseline launcher (pinned);
- the answer on the config hazard.