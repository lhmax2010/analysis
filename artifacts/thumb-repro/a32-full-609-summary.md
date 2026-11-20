# A32 cohort for the 17 November KantSU2E PERF image

The retained scan of the 2,342 installed-RPM roster reports 5,166 loadable ELFs, 609 ARM-predominant files and 343.1 MiB of estimated A32 code. The top 211 hold about 333.2 MiB and the remaining 398 hold about 9.9 MiB. There are 38 sub-KiB rows in the tail, flagged `tiny`. The CSV's floor-rounded row estimates sum to 342.81 MiB and the floor-rounded tail to 9.75 MiB. These values describe file code estimates. They do not measure PSS. [Native scan readback](../evidence/native-run-r0010-a32full-olevel-20261120.txt)

Ranks 1–211 reproduce archived Doc 07 and retain its reported share precision. The native return covers ranks 212–609 only. The original top-40 preview permits an independent partial rank, path and estimate check. The basis for ranks 1–211 stays `NOT_RETURNED` until the native export. The aggregate rounded share matches the report. [Doc 07](../../reports/weekly/2026-11-20/07_HQ_Table_A32_Files.md) [Top-40 preview](../evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L104)

## Doc 07 reconciliation

- Rank 8 `est_a32_kib` `8152` → `8149`.
- Rank 9 `est_a32_kib` `6217` → `6215`.
- Rank 10 `est_a32_kib` `6210` → `6212`.
- Rank 11 `est_a32_kib` `5045` → `5047`.
- Rank 16 `est_a32_kib` `3801` → `3803`.
- Rank 19 `est_a32_kib` `2709` → `2708`.
- Rank 20 `est_a32_kib` `2662` → `2661`.
- Rank 22 `est_a32_kib` `2335` → `2334`.
- Rank 28 `est_a32_kib` `1480` → `1479`.
- Rank 29 `est_a32_kib` `1428` → `1427`.
- Rank 36 `est_a32_kib` `1235` → `1234`.
- Rank 37 `est_a32_kib` `1225` → `1224`.
- Rank 38 `est_a32_kib` `1224` → `1223`.
- Rank 39 `est_a32_kib` `1199` → `1198`.

The values from the 0010a -O summary and Doc 07 have different scopes. The former sums the loadable executable sections across the RPM and the latter prints individually floored file estimates. The native per-file export is the remaining independent check for ranks 41–211, including exact mode basis and identity. Doc 07 uses decimal MB in its introductory total and MiB for class totals. All class and family totals in this working table use MiB.

The eight cause classes remain evidence tiers for follow-up. The Clang category is an A32 candidate category based largely on markers, with actual mode flags and object origin still pending. GCC/assembly/prebuilt/wrapper exceptions require producer and package records. Across all 12 explicit -marm labels, seven have qualifying path-and-owner DWARF producer evidence. Six are in the top 211 (13, 14, 36, 38, 58, 59) and one is in the tail (361). The five Bluetooth paths below lack a qualifying -marm producer match in the retained table. Their existing Doc 07 attribution remains provisional.

- Rank 5 bluetooth-impl-sec-oal `/prd/usr/lib/libbluetooth.so`.
- Rank 20 bluetooth-impl-sec-oal `/prd/usr/lib/libleaudio.so`.
- Rank 50 bluetooth-impl-sec-oal `/prd/usr/lib/librtkbt_ss_da.so`.
- Rank 160 bluetooth-impl-sec-oal `/prd/usr/lib/libbt-vendor-aic.so`.
- Rank 195 bluetooth-impl-sec-oal `/prd/usr/lib/librtkbt_vendor.so`.

## Estimated A32 by cause

| Cause class | Files | Est. MiB | Tail files |
|---|---:|---:|---:|
| Clang A32 candidate (effective mode cause pending) | 442 | 131.52 | 309 |
| Bundled prebuilt | 5 | 128.97 | 0 |
| GCC-built: prebuilt, assembly or wrapper-exempt | 76 | 30.14 | 27 |
| Explicit -marm | 12 | 26.07 | 1 |
| Prebuilt (argot/cargo-tizen) | 2 | 11.24 | 0 |
| No compiler marker | 3 | 9.66 | 1 |
| Base GCC build without the wrapper | 67 | 4.06 | 60 |
| Rust-built, target not verified | 2 | 1.14 | 0 |

## Estimated A32 by package family

These mutually exclusive groups prioritize archive members before package families. Families are for triage. Compiler markers and similar filenames alone leave a common build-rule cause open. The retained DWARF includes Chromium Crosswalk extension sources and separate ARM assembly units. The shelf history also names `webapi-microphone-pepper-plugin/src/microphone/microphone.gyp`. This is a per-plugin build file, and the evidence does not establish a single shared rule dropping CFLAGS. Read the actual GYP/CMake includes and representative compile lines before attributing this family-wide. [Crosswalk sample](../evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L443)

| Family | Files | Est. MiB | Tail files |
|---|---:|---:|---:|
| vd_memps bundled tools | 5 | 128.97 | 0 |
| Other | 185 | 86.07 | 119 |
| TPK content | 75 | 41.29 | 21 |
| Bluetooth | 13 | 23.82 | 4 |
| DRM / player | 12 | 17.03 | 2 |
| GStreamer | 41 | 13.73 | 28 |
| WebAPI / Crosswalk | 94 | 11.04 | 70 |
| PERF RPMs (loadable ELFs) | 10 | 7.69 | 3 |
| Base open source | 28 | 4.62 | 22 |
| glibc / locale | 67 | 4.06 | 60 |
| sys-tools | 66 | 3.05 | 60 |
| Boost | 13 | 1.43 | 9 |

## Installation evidence

| Evidence | Files | Est. MiB | Tail files |
|---|---:|---:|---:|
| INSTALLED_RPM_PAYLOAD | 586 | 316.80 | 389 |
| FILE_OBSERVED | 23 | 26.01 | 9 |

`FILE_OBSERVED` joins retained exact board path and RPM owner evidence. `INSTALLED_RPM_PAYLOAD` joins the ELF payload to its installed RPM header SOURCERPM on the observed PERF board. An installed RPM can contain preload archive members, and this status leaves per-file on-disk verification open. Preserve this distinction when reporting actual runtime residency or presence in a future production release.

`sys-tools-0-0.armv7l`, `wifi-drivers-MTK-7668-perf`, `vdlinux-usb-modules-perf`, `zone-manager-perf`, `playready-test` and `widevine-cdm-test` are in the recorded board RPM inventory. The `sys-tools` payload has ARM32 application and Python side libraries in this build. The Doc 05 build-host-only statement does not apply to the measured PERF board. Evidence for inclusion in a retail build remains open. [Installed header roster](../ledger/README.md)
