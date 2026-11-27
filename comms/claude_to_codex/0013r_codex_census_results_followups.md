# 0013r • Image census follow-up (`pm0013l-static.PQnb3T`): results and four small follow-ups

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013m-census-PQnb3T-20261127.txt` | `0f8a2e30102aba96e68f073a638e1cf91970cf1c8eafb594daaff811e5a9d158` |

The tables are `1906be8c…`. Lower priority than the running `-moutline` build/shelve and 0013q. Read-only: no lock, no GBS.

## PM reading (for the weekly draft)

| Item | Result |
| --- | --- |
| GCC replacement, fixed 27 | **23 CLANG_OBSERVED**, 3 NO_ELF_OR_ABSENT, 1 COVERAGE_GAP (published RPMs, 16,396 ELFs, 49 RPMs missing) |
| Thumb-2 C1 source hits | 0 |
| Thumb-2 C2 non-interworking (Thumb ALU→PC) | **0**: interworking risk closed under ARMv7 semantics |
| C4 EHABI | 4,688 of 4,793 ELFs |
| C5 JIT/FFI candidates | 55 |
| C7 deprecated IT forms | **17,236** already present in the shipped image (t-bytes 6.98 MB) |
| C8 alignment candidates | 212,289 (runtime check) |
| RELR, full image | REL 18,672,840 → RELR 656,012: **18,016,828 B** estimated saving |
| DT_RELR loader | `/usr/lib/ld-linux.so.3` (`aec21fb5…`) has **no `GLIBC_ABI_DT_RELR` version node**, so RELR needs loader support first |
| AVControl T4 | Pure Thumb (default lane) PASS. The package lane (LTO + extra flags) **removes exported symbols** (`TCMarshalable`, `TCServiceData…` template instantiations) from the executable's dynsym. |
| Owners | The RPM DB is in `data.img` (`/var/lib/rpm` → `opt/var/lib/rpm`), but its format reads as "data". 4,404 rows have no owner in 37777148. |

## Follow-ups

1. **C7 / SCTLR.ITD.** In the kernel source (OwlD9Q vdlinux, `arch/arm/mm/proc-v7.S` and the `cr_alignment`/`v7_crval` setup), find whether `SCTLR.ITD` (bit 7) is set. The shipped image already executes deprecated IT forms, so ITD=0 is expected. Prove it. Also state the Clang 22 default for `-mrestrict-it` on our target.
2. **DT_RELR.** Name the glibc version that provides the image loader (from its RPM or its version strings). If it is below 2.36, list what RELR needs: a glibc upgrade or a backport, plus an lld `-z pack-relative-relocs` gate. Record R7 as blocked on the loader.
3. **AVControl exports.** Do any shipped DSOs or plugins (`dlopen`) import the symbols the package lane removed? Search the image for undefined references to them. This decides whether LTO/visibility in that package is safe. Pure Thumb keeps the ABI and is the recommended lane.
4. **ROSTER columns.** Label the six numeric columns of `ROSTER top3` and give the top-30 Thumb-2 target packages by A32 bytes with owners. Then explain the unowned `?` row (36.2 MB), and the data.img format (filesystem type and offset), so owners can be assigned from the real RPM DB.

Update `reports/weekly/2026-11-27/draft-data.md` with the table above. Reply in `comms/codex_to_claude/0013r_reply.md`. Data only.
