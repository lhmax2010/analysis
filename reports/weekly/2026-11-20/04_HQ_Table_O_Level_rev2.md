# HQ Table — Packages Below the Global Optimization Level

Nov 20, 2026 · @Hao

34 packages build below `-O2`: 21 at `-Og`, 9 at `-O0`, 2 at `-O1` / `-O`, libpisa-ipc below `-O2` (its CFLAGS are replaced), and libgcrypt with 4 files at `-O0` / `-O1`. Our fix moves them to `-Os`, the LLVM global level. On the 4 packages measured so far, it reduces `.text` by 20% to 76%. Packages that set `-O2` or `-O3` themselves are out of scope and keep their level.

In the current LLVM image none of the 34 has been changed yet. The fix for rows 1–4 is validated in local builds but is not yet in a QuickBuild; all 34 still build at their own level.

**How the list is built.**

- **Scope:** every package whose effective level is below the global level, both the 4 packages our forced-option change already covers and the remaining ones.
- **GCC lane:** in the GCC image, the `gcc-warning-build-env` wrapper appended `-O2` to non-exempt Product packages, overriding their own level. Base packages have no wrapper.
- **LLVM image now:** Clang has no wrapper, so each package builds at its own level.
- **Our fix:** the Clang forced-option hook (`%clang_force_incompatible`) appends `-Os` with `-mthumb`, the target and hardening options and `-fsigned-char` to non-exempt packages (no warning options). Packages on an exemption list are changed in their own spec.

## Per-package list

| # | Package | Source | Own level | Forced -O2 in GCC lane | LLVM image now | After our fix | .text now (KB) | .text after fix (KB) | GCC image .text (KB) | Effect of fix | Status |
| ---: | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | org.tizen.AVControl | Product | -O0 (no level in spec) | Yes | -O0 | -Os (Clang forced options) | 720 | 173 | 245 | −76.0% | Validated locally; build.conf change ready |
| 2 | org.tizen.tv-viewer | Product | -O1 | Yes | -O1 | -Os (Clang forced options) | 4,630 | 2,362 | 4,080 | −49.0% | Validated locally; build.conf change ready |
| 3 | org.tizen.webappservice | Product | -O (= -O1) | Yes | -O | -Os (Clang forced options) | 6,534 | 5,210 | 2,808 | −20.3% | Validated locally; build.conf change ready |
| 4 | libpisa-ipc | Product | below -O2 (CFLAGS replaced) | Yes | below | -Os (Clang forced options) | 877 | 399 | 478 | −54.5% | Validated locally; build.conf change ready |
| 5 | machine-learning-api | Product | -O0 | To confirm (exemption list) | -O0 | -Os | — | — | — | To measure | Coverage build in %if branch: confirm |
| 6 | nnstreamer | Product | -O0 | To confirm (exemption list) | -O0 | -Os | — | — | — | To measure | Coverage build in %if branch: confirm |
| 7 | rpm | Base | -O0 | No (Base, no wrapper) | -O0 | -Os | — | — | — | To measure | Owner check |
| 8 | source-service | Product | -O0 | To confirm (exemption list) | -O0 | -Os | — | — | — | To measure | Coverage build in %if branch: confirm |
| 9 | vulkan-utility-libraries | Product | -O0 | To confirm (exemption list) | -O0 | -Os | — | — | — | To measure | Owner check |
| 10 | vulkan-validation-layers | Product | -O0 | To confirm (exemption list) | -O0 | -Os | — | — | — | To measure | Owner check |
| 11 | org.tizen.webserver | Product | -O0 (make files add -O0 -g3) | To confirm (exemption list) | -O0 | -Os | — | — | — | To measure | Owner check |
| 12 | libiri | Base | -O0 | No (Base, no wrapper) | -O0 | -Os | — | — | — | To measure | Owner check |
| 13 | libgcrypt | Base | -O0 / -O1 on 4 files (on purpose) | No (Base, no wrapper) | -O0 | Keep (intended) | — | — | — | To measure | Keep |
| 14 | mmi | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 15 | mmi-plugins-default | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 16 | org.tizen.rct-app | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 17 | org.tizen.reminder | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 18 | rct-service | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 19 | reminder-api | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 20 | reminder-service | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 21 | tvs-api | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 22 | tvs-api-native | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 23 | tvs-chms | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 24 | tvs-core | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 25 | tvs-dbms | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 26 | tvs-dvb-chms | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 27 | tvs-dvbbase-chms | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 28 | tvs-ewbs | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 29 | tvs-ht | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 30 | tvs-iss | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 31 | tvs-list-app | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 32 | tvs-nrt | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 33 | tvs-util | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
| 34 | ug_rct | Product | -Og | To confirm (exemption list) | -Og | -Os | — | — | — | To measure | Owner check (debug level in release) |
Measured rows 1–4 come from the 11 Nov local rebuilds with the Clang forced-option hook. Its expanded value in the 11 Nov build logs also appends -mthumb, so rows 1, 2 and 4 include the A32 → Thumb-2 change: AVControl, tv-viewer and libpisa-ipc are A32 in the current image, while webappservice (row 3) is already Thumb-2; all four packages together: loaded sections 17,540 → 12,992 KB (−25.9%). The other rows are rebuilt and measured in the option re-run next week. Sources: the spec scan of 181 spec files and the Base build logs (`-O` of every compile command).
