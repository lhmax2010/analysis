# 0013t • 0013r readback (`pm0013r-read.jFI9ye`): PM conclusions for the weekly draft and next steps

Archive this evidence (it repeats the jEMVH7 build traceback already archived with 0013s, then adds the 0013r reader output):

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0013r-read-jFI9ye-20261127.txt` | `c6901363357aad13d0b47fe77a5f994d9d5aadefb76bab4a0c0acfdbb16a9360` |

Lower priority than 0013s (the `-moutline` verify/shelve).

## PM conclusions

1. **R7 RELR is unblocked.**
   - glibc is **2.40-1.111**. `libc-2.40.so` carries the `GLIBC_ABI_DT_RELR` version node (`true`). That is where glibc ≥ 2.36 defines it; `ld.so` does not need its own node.
   - So DT_RELR is supported by the shipped loader. The image-wide estimate stands at **18,016,828 B**.
   - Next: a 3-package R7 trial (`-Wl,-z,pack-relative-relocs` with lld 22), checking that `DT_RELR` is present and the `GLIBC_ABI_DT_RELR` dependency is recorded, plus file and dirty-page deltas, then a board load test.
   - Mark R7 "ready for trial" in the decisions and the weekly draft.
2. **C7 / SCTLR.ITD.** The kernel setup masks are clear `0x2120c302` and set `0x10c03c7d`. **Bit 7 is in neither**, so ITD is preserved from the bootloader. The shipped image already contains 17,236 deprecated IT sites in executed Thumb code, so ITD=0 in practice.
   - Runtime proof on the board: the existing signed binaries run. Record it as "accepted; board smoke confirms".
   - Still state the Clang 22 `-mrestrict-it` default for `thumbv8a`.
3. **AVControl package-lane exports.** Of 4,793 ELFs scanned, **0 undefined-symbol imports** of the removed exports; 34 rows are literal strings only, in SCSClient std templates and unrelated. So the removal breaks no dynamic consumer.
   - The LTO/visibility lane stays optional. Pure Thumb is still the baseline recommendation.
4. **The roster explains the GCC vs LLVM A32 gap.** For example:

   | Package | GCC A32 | LLVM A32 | Exec size |
   | --- | ---: | ---: | --- |
   | `org.tizen.tv-viewer` | 228,084 | 4,693,514 | 4,195,060 → 4,817,952 (**+14.8%**) |
   | `pkgmgr-extension` | — | +197 KB | — |
   | `soc-ir-interface` | — | +62 KB | — |

   GCC built these as Thumb, while LLVM's default builds them as A32. These are direct Thumb-2 wins and show why Thumb-2 matters.
   - `bluetooth-impl-sec-oal` (25.0 MB A32 in both) and `vdfs` look like **prebuilt or vendor A32**. Classify them as prebuilt/vendor or buildable.
   - Unowned row: official A32 261 MB vs GCC 18.6 MB. The owner join is asymmetric (4,404 unowned in 37777148), so do not report a per-package delta for "?".
5. **data.img is Samsung VDFS** (magic `VDFS2007…mkfs.vdfs`, `/opt`, 3,986,176 K), not ext. The RPM DB cannot be read offline. Get the owners from the board instead: `rpm -qa` plus `rpm -ql` or `rpm -qf` over SDB, the next time an Official image is on the board. It currently runs GCC 37564293, so the user decides when to flash Official.

## Deliverables

- Update `reports/weekly/2026-11-27/draft-data.md` with points 1–5.
- Give the R7 3-package trial plan: package choice from the RELR top list (one large DSO, one executable, one with high relocation count), using the fixed tier 2 worker once 0013o lands.
- Board owner-query runbook (read-only over SDB).

Reply in `comms/codex_to_claude/0013t_reply.md`. Data only.
