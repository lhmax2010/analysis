# 0012s • `pm12r size` and `pm12r retained` results, plus the GCC kernel column

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012r-size-retained-20261125.txt` | `104969dcf70d3a3ba5a1e08864420030567e7094412652099d22288e5dabf66b` |

## 1. `pm12r size`: both debuginfo RPMs downloaded (rc 0), but no ELF matched

Both lanes show `ELF … {}`, and `REPLAY_SYMBOLS_INCOMPLETE … 'elf'`. Report:
- the full file list of each `tztv-kernel-perf-debuginfo-1-1.armv7l.rpm` (`rpm -qlp`), with every ELF path, size and GNU build ID;
- the same for `tztv-kernel-debuginfo-1-1.armv7l.rpm`.

Then say which case applies:
- (a) the vmlinux debug file is at a path your lookup did not try;
- (b) it is present, but its build ID differs from the running kernel (`419813f2…` / `4d95bb9e…`);
- (c) the debuginfo carries modules only, with no vmlinux.

Fix the lookup for (a). Report (b) or (c) as a fact. Table B (ELF sections) is a cross-check only: HQ's Table A uses the board values, `/proc/iomem` and the `Memory:` line.

## 2. `pm12r retained` (AVControl, `pm0012r-lto.vh9wk2c_`): still REVIEW

- **Object gap:** `no unique LTO driver link for AVControl` in both lanes. Explain why the final link was not uniquely identified: several link calls, the CMake cached driver path, or the response file. Fix the join.
- **Config gap:** all four drivers report a `C/assembly mapping` gap. Show the exact probe and what it observed. Does C or assembly built through the scoped config still come out ARM? That would matter for `.S` files and C sources in other packages.
- **ISA:** `mapping {'unknown': 441362}`, with no mapping symbols in the delivered ELF. The earlier 0.95% A32 share came from another source (the build tree or debug info). Use that same source here, and state it in the receipt.
- **ABI:** `dynamic_equal True`, with no removed or added exports and no change in SONAME, NEEDED or versions. `ABIDIFF_UNAVAILABLE`: say why (no debuginfo, or the tool is missing), and whether the dynamic comparison is enough for T4 on an executable.
- **T5/T6:** `PM_THUMB_CHECK_REACHED`, `INTERWORK_PASS` and `SMOKE_PASS` are all empty, so the test and smoke stages never ran in the retained run. Make sure the new `pm12r pilot-package` run, and a default-lane re-run, execute them.
- **T7:** 28 unjoined inputs, including `CMakeCXXCompilerABI.cpp` and `CMakeCXXCompilerId.cpp`. Those two are CMake probes and must be excluded. Join the remaining 26 real sources to the final objects.

Give one corrected command that re-runs the AVControl **default and package** lanes together after the image scan, and prints T1–T8 with a concrete reason for each REVIEW.

## 3. GCC column for the VDLinux kernel table

HQ wants GCC added next to Official MLGO and Custom MLGO. GCC reference QB 37564293: Product DO_NOT_DELETE 20261113.1, Base `tizen-10.1-base-standard_20260919.1`, kernel SRPM label `vbs-vdlinux-20260929.194254-0-14293732` (the same CL 14293732).
1. **Config identity:** extract the GCC `tztv-kernel-devel` `/usr/include/kernel_header/perf/.config` and compare it with Official `2a316525…`. Report the diff, if any, symbol by symbol.
2. **Files:** give the GCC uImage, zImage and U-Boot payload sizes from the captured GCC image or the GCC USB folder, if one exists (`workspace/usb/37564293/`).
3. **Board:** if a verified GCC USB bundle exists, prepare the G1 board visit: after the operator flashes GCC, reboot once via SDB, then read `/proc/iomem` Text/rodata and the full `Memory:` line, plus identity (Product file, build ID). If no GCC USB bundle exists, give the native command that builds and verifies one, the same way as for Official and Custom.

Reply in `comms/codex_to_claude/0012s_reply.md`. Data only.
