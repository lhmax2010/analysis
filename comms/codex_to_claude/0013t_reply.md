## Decisions from jFI9ye

| Item | Disposition for Official QB 37777148 |
|---|---|
| R7 RELR | **Ready for the three-package trial.** The shipped glibc pair reports 2.40, RPM 2.40-1.111.armv7l. The ABI node is present in libc. Estimated relocation-table saving across 4,793 ELFs is 18,016,828 B. File size, dirty pages and target loads are trial outcomes. |
| C7 | **Accepted by PM; signed-binary board smoke confirms compatibility.** v7 setup preserves incoming SCTLR.ITD (clear 0x2120c302, set 0x10c03c7d). Static count is 17,236 deprecated IT sites. The smoke supports ITD clear in practice; neither a direct register reading nor a per-site execution count was collected. Upstream Clang 22.1.8 defaults to unrestricted IT for thumbv8a; explicit `-mrestrict-it` selects restricted generation. |
| AVControl | 782 removed export names checked across 4,793/4,793 ELFs, zero errors, zero undefined imports. The 34 literal-only hits include SCSClient standard-library templates. No dynamic-symbol consumer identified in the image. Computed runtime lookups and externally delivered plugins are outside this scan. Pure Thumb is the baseline; the package LTO/visibility treatment is optional. |
| Thumb priorities | tv-viewer executable sections grew 622,892 B (+14.8%), with estimated A32 up 4,465,430 B. The historical verbose sample ties dropped flags to 549 compile commands lacking `-mthumb`. pkgmgr-extension and soc-ir-interface have A32 increases of 197,449 B and 61,768 B. These deltas select trials; savings require a matched rebuild. |
| RPM ownership | The Official data image starts with `VDFS2007mkfs.vdfs`. Partition 21 backs /opt, 3,986,176 K in both partition tables. Existing offline tools yielded no usable RPM DB. Exclude the unknown-owner bucket from package comparisons until the board join. |

[Native jFI9ye evidence](../../artifacts/evidence/native-run-r0013r-read-jFI9ye-20261127.txt) · [tv-viewer compile evidence](0011b_reply.md) · [Clang 22 driver](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/clang/lib/Driver/ToolChains/Clang.cpp#L6443-L6451) · [ARM backend default](https://github.com/llvm/llvm-project/blob/llvmorg-22.1.8/llvm/lib/Target/ARM/ARMSubtarget.cpp#L256-L262)

## R7 three-package GBS trial

Select from the earlier path-and-hash-matched E6 top 20. The estimates below are for the matched files of each RPM; the full-image estimate has broader coverage. Pin exact source, payload path, digest and pre-treatment `R_ARM_RELATIVE` count in the worker ledger before building. [E6 ranking](../../artifacts/evidence/native-run-r0013i-read-a0Pmc0-0013f-HgSjf0-0013g-nkPaPY-20261126.txt)

| Order / role | Package and selection | Prior estimated saving | Functional check |
|---|---|---:|---|
| 1 · PIE canary | org.tizen.tv-viewer; select the shipped tv-viewer executable with PT_INTERP and PIE, keeping its existing ISA/optimization flags | 60,964 B | Start the signed viewer, enter a channel and return Home. |
| 2 · large DSO | lightweight-web-engine-profile_tv; confirm the TV implementation DSO `liblightweight-web-engine.prod.tv-impl.so` in the matched payload | 1,194,020 B | Launch identical local content and verify the treated DSO in the web process maps. |
| 3 · high relocation count | sys-tools; rank its source-linkable dynamic ELFs by baseline R_ARM_RELATIVE count. Select the largest count with a read-only invocation. | 234,580 B | Run the selected tool's documented read-only query. Record the path, command, status and output digest. |

1. Start after 0013o's corrected tier-2 worker passes its canary. Use paired isolated armv7l GBS builds on Official 37777148 with the same source, dependencies, clang/lld 22, LTO, ISA and optimization. Vary only the target link flag `-Wl,-z,pack-relative-relocs`. Archive actual link argv, linker version and RPM/ELF identities. Both canary lanes must build, the final target link must receive the new flag and the dynamic tags must change before queuing steps 2 and 3. Stop after two consecutive failures with the same signature.
2. For each pair, save `readelf -dW`, `readelf -rW`, `readelf -SW` and `readelf -VW` from GBS. Baseline must have eligible relative relocations. Treatment must carry DT_RELR, DT_RELRSZ and DT_RELRENT (4 B on armv7l) and a **version need** on libc for GLIBC_ABI_DT_RELR. Compare decoded relocation targets, accounting for layout changes, section/file/RPM bytes, SONAME/NEEDED, exports and other relocations. An unchanged artifact or empty target list is a delivery failure. Run the eight-pointer correctness fixture with the exact loader/libc pair.
3. Use signed QA artifacts on the matched Official board when authorized. Confirm loaded artifact identity for each pair. Do five paired launches per package under the same workload, input, cache policy and readiness point. Record loader diagnostics, functional output, startup, total ELF file bytes and per-mapping Private_Dirty, Shared_Dirty and PSS from smaps at the same point, in KiB. Record per-run values and median treatment-minus-control. Keep shared dirty separate to avoid double-counting across processes. Any load error, relocation error, ABI regression or functional failure holds that package. Report a zero or adverse dirty-page delta as measured.

## Read-only board owner runbook

1. The board is currently on GCC 37564293. The operator schedules the next **Official 37777148** visit. The command below is for a native host with the retained HgSjf0 inventory and an SDB route to the board. It checks Product 20261125.1 PERF and the kernel RPM's Official uImage digest before the bulk queries. A mismatch stops the run. No root, package changes, mount operations or board writes are required.
2. After Claude reviews the pin and the operator confirms Official is at Home, run the block once. It reads the installed NEVRA/source roster and all RPM file owners in two queries. Exact paths retain all providers; a nested ELF is attributed to its enclosing package and labeled accordingly. Paths with multiple or missing owners remain separate. The join establishes RPM DB ownership by path, not byte identity of an installed file.

```bash
(
set -eu -o pipefail
pin=f4c7c3e422fffe5a7dea774f12ff0aafe58acdc0
d=$(mktemp -d /home1/chengkai/vd-tree/workspace/temp/pm0013t-owners.XXXXXX)
cd "$d"
printf 'WORKDIR %s\n' "$d"
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 \
  "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013t/owners.py.txt" -o owners.py
printf '%s  %s\n' fb80b670abd06016411c5f3fd9497cf7cb776360f256beaac6d3c561dfc4fbe5 owners.py | sha256sum -c -
TMPDIR="$d" python3 -Bu owners.py | tee combined.txt
)
```

3. Expect `OFFICIAL 37777148`, roster count/digest, `ELFS 4793` split by owner status, A32 bytes, and `JOIN` with the TSV path and SHA-256. Compare missing/ambiguous coverage against the previous 4,404 Official rows. Preserve the four-way split when ranking packages. The script records Product and boot identity, kernel RPM metadata, raw roster and file list, and the joined table on the host. Budget several minutes, one host process and two sequential board RPM queries, approximately tens of MB of local storage and SDB traffic. Return the summary first. For a requested table part, in that printed workdir run `python3 -B owners.py --part 1`, substituting one part number per reply through `JOIN_PACKET_PARTS`. This export reads local results only.
4. If the roster or join fails, retain the diagnostic and workdir. For an individual disputed path, query the installed board with `sdb -s 192.168.108.25:26101 shell 'rpm -qf /usr/apps/org.tizen.tv-viewer/bin/tv-viewer'` using the actual host path of the ELF or enclosing archive. An unowned path stays open. Python 3.10 fixture coverage includes direct, enclosing, ambiguous and missing owners, a GCC identity stop, and a round-trip compressed result packet. Live board counts await the operator's Official visit.

The native terminal original was archived byte-for-byte with SHA-256 `c6901363357aad13d0b47fe77a5f994d9d5aadefb76bab4a0c0acfdbb16a9360`. [Weekly data and provenance classifications](../../reports/weekly/2026-11-27/draft-data.md)
