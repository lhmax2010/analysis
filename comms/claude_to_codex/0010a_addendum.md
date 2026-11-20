# 0010a — Claude (PM) → Codex: r0010 readback (full A32 list + current code of the -O packages)

Date: 2026-11-20. Adds to 0010 (Task A backup, Task B -O launcher, Task D next-week plan stay as written). This round replaces 0010 Task C with the concrete work below, and adds two changes to Task B.

## Evidence (archive first)

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0010-a32full-olevel-20261120.txt` (attached; verbatim user terminal output, last line is the shell prompt) | `5c0554c8932bbfdfb401f4810035b9b8b25eb8ad3ca712a5e44fd2d13e51032f` |

Inside the output:
- scanned CSV `pm0004-image-mode.b7rJie/results/elf-modes.csv`, SHA-256 `d6fd74fe1dd6bdbe1db2cf52482010169c379bdc785672c4e16935118e5bdecf`
- native output file `workspace/temp/pm0010-a32full-olevel-20261120-205401.txt`, SHA-256 `5d3fede77cb432f8301a52cba9786af0d9b4f9ad7530d490bce6345edb3432a4`

## What the readback proves (my review)

1. `CHECK loadable=5166 arm_predominant=609 a32_est_MiB=343.1 top211_share=0.971`. The file count and the 97% share match Doc 07. 343.1 MiB = 359.7 MB (decimal), so the "359.7 MB" in Docs 01/07 is correct, but the Doc 07 cause table is in MiB (top 211 = 333.2 MiB). From now on use **MiB everywhere** in the A32 tables: 343.1 MiB total, 333.2 MiB in the top 211, 9.9 MiB in rows 212–609.
2. Rows 212–609: 398 files, 10,180 KiB of estimated A32 code by marker (309 GCC+Clang / 8,496 KiB, 88 GCC / 1,680 KiB, 1 none / 4 KiB). Rank 212 is 121 KiB, which confirms "each under 122 KiB".
3. A first family grouping of rows 212–609 (by my script on the readback; per-row KiB is floored, so the total is 9,984):

| Family | Files | Est. A32 KiB | Markers |
| --- | --: | --: | --- |
| webapi / crosswalk plugins | 70 | 3,327 | 69 GCC+Clang, 1 GCC |
| other | 107 | 2,498 | 96 GCC+Clang, 10 GCC, 1 none |
| TPK content | 21 | 856 | 8 GCC+Clang, 13 GCC |
| gstreamer plugins | 28 | 764 | GCC+Clang |
| sys-tools (python3.5 lib-dynload, coremark, …) | 60 | 690 | GCC+Clang |
| Base open source (dbus, rpm, systemd, util-linux, gawk, libcap, …) | 39 | 683 | GCC+Clang |
| glibc / glibc-locale (gconv) | 60 | 625 | GCC |
| boost | 9 | 365 | GCC+Clang |
| bluetooth-impl-sec-oal | 4 | 176 | GCC |

   38 rows have under 1 KiB of A32 code (MIXED_ARM near the 0.5 threshold); keep them in the CSV but flag `tiny`.
4. **The -O packages and A32 overlap.** The current-image `O` lines show that the large -O packages are also almost fully A32:

| Package | Files | Code KiB | A32 KiB |
| --- | --: | --: | --: |
| org.tizen.AVControl | 1 | 723 | 723 |
| org.tizen.tv-viewer | 2 | 4,918 | 4,796 |
| libpisa-ipc | 6 | 894 | 894 |
| org.tizen.webserver | 3 | 1,596 | 1,595 |
| libgcrypt | 1 | 648 | 647 |
| rpm | 13 | 2,672 | 2,665 |
| nnstreamer-tensorflow2-lite | 1 | 6,223 | 6,215 |

   The tvs-* packages, webappservice and source-service are Thumb. This fits one mechanism: a package that replaces `$CFLAGS` with its own `-O` also drops `-mthumb`. So the 11 Nov "gap closed" result in Doc 04 rows 1–4 (AVControl −76%, tv-viewer −49%, libpisa-ipc −54.5%) very likely combines two effects, the level change and A32 → Thumb-2. HQ will ask which part comes from which, so we must split them.
5. **Ten -O packages have no loadable ELF under that RPM name:**
   `machine-learning-api vulkan-utility-libraries vulkan-validation-layers mmi mmi-plugins-default org.tizen.rct-app rct-service tvs-core tvs-list-app ug_rct`
   Some are clearly name mismatches between the spec name and the binary RPM name (`ug_rct` vs `ug-rct`, and `tvs-core` vs `libtvs-core`, both of which appear in Doc 05). Others may not ship in this product. Prefix matching also pulled in sub-packages that may come from another source (`rpm-security-plugin`, `nnstreamer-tensorflow2-lite`).

## Task C (replaces 0010 Task C) — full 609-file A32 table

1. Archive the evidence file above and check its SHA-256.
2. Build `artifacts/thumb-repro/a32-full-609.csv` with these columns:
   `rank, package, source_rpm, path, code_kib, a32_share, est_a32_kib, basis, markers, cause_class, family, installed_in_perf_image, tiny`
   - Ranks 1–211: take the 211 rows as given and check them against Doc 07 (backup copy `reports/weekly/2026-11-20/07_HQ_Table_A32_Files.md`). Report every mismatch.
   - Ranks 212–609: take them from the r0010 readback, with the same eight cause classes as Doc 07. Base the class on `thumb-causes.py` logic, DWARF producer `-marm` (`retained-board-arm-baseline.csv`) and package origin.
   - Classes I expect from the readback:
     - glibc / glibc-locale → "Base GCC build without the wrapper";
     - bluetooth-impl-sec-oal → "Explicit -marm" if DWARF confirms it;
     - GCC-only TPK content (smartthings plugin, mcp_server_app, csft-service, …) → "GCC-built: prebuilt, assembly or wrapper-exempt";
     - tvp-tv `libFPSTee.so` → "No compiler marker".
   - `source_rpm`: from the RPM header SOURCERPM. Do not use name prefixes.
   - `installed_in_perf_image`: whether the file is in the PERF image root filesystem / preload TPKs. The scan covers every RPM of the build. sys-tools, the `*-perf` packages (wifi-drivers-MTK-7668-perf, vdlinux-usb-modules-perf, zone-manager-perf) and the test packages in the top 211 (playready-test, widevine-cdm-test) may not ship in a release image. Doc 05 already calls sys-tools "build-host package, not installed on the TV", while this scan shows TV-side paths for it. Resolve this contradiction with evidence.
3. Commit a summary `artifacts/thumb-repro/a32-full-609-summary.md` covering all 609 files:
   - files and MiB per cause class;
   - files and MiB per family, focusing on root causes shared by many packages. For example, the crosswalk/webapi plugin family has 70 files in rows 212–609 plus many in the top 211; find out whether one common build file (gyp/CMake template) drops `$CFLAGS`, and name it;
   - files and MiB that are actually installed in the PERF image.
4. If a ready read-only command is needed for (2), for example `rpm -qp --qf '%{SOURCERPM}'` over the retained RPM set or a PERF image file list, give the user one copy-paste native command with compact output (under 150 lines) and a SHA-256.

## Task B changes (the -O launcher from 0010)

1. **Package mapping.** Map each Doc 04 source name to its binary RPMs and shipped ELF files through SOURCERPM (spec → SRPM → RPMs). Report the mapping per package and mark the ones not shipped for this product as `NOT_SHIPPED`. Build only the shipped ones; list the others with the evidence.
2. **Split the level effect from the ISA effect.** Use three lanes instead of two:
   - **A:** unchanged (now).
   - **B:** level only. Append `-Os`, keep the package's current ISA, and add none of the other forced options.
   - **C:** the full 11 Nov forced-option set.
   
   Before building, state whether the 11 Nov `%clang_force_incompatible` option string contains `-mthumb`, and quote it.
   
   Run lane C on: the packages with A32 share over 50% (AVControl, tv-viewer, libpisa-ipc, webserver, libgcrypt, rpm, nnstreamer), and on all of rows 1–4 again so the published numbers can be split. For packages that are already Thumb, B and C differ only by hardening and `-fsigned-char`; C is still useful but lower priority.
   
   The readback line becomes:
   `O <pkg> | A .text | B .text | C .text | ΔB% | ΔC% | A loaded | B loaded | C loaded | A32 share A/B/C | CU levels A/B/C | status`
3. Add the current-image numbers from the r0010 `O` lines to the readback header, so the A lane can be checked against the image (A lane `.text` ≈ image, as on 11 Nov).

## Reply

In `comms/codex_to_claude/0010_reply.md` (or `0010a_reply.md` if 0010 was already answered), give:
- the Task A result;
- the Task C files and their SHA-256;
- the mismatches found against Doc 07;
- the source-name → RPM mapping for the 34 -O packages;
- the updated Task B launcher (commit + SHA-256) and its run command;
- the Monday commands in run order.