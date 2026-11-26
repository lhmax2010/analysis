## 1. Native host now · B + C + E · read-only inputs, no build lock, GBS or sudo

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree/workspace/temp
  d=$(mktemp -d "$PWD/pm0013-get.XXXXXX")
  pin=9047570ba80a43965d92ce90b8b38ffb8664e946
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 150 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013a/run.sh.txt" -o "$d/run"
  printf '%s  %s\n' fca915876ba930af427c82b62016effa99c80ea12082059dbc22865742c24f42 "$d/run" | sha256sum -c -
  bash "$d/run" "$pin" 152a1274626f1cba04662ef9d88a6aefdae4133faabb522a8fc3c2968711ff68 bce
)
```

E starts independently of the vendor reader. C extracts one partition at a time. B reuses the three retained AVControl lanes and can use the image ELF from C or the pinned Official RPM. A failure in one section is recorded independently. Start in a persistent terminal. Allow several hours for the full Product and Base scans including debuginfo. B and C share one low-priority worker, E uses a second. Traffic depends on the total published RPM payload. C checks the 50 GiB reserve plus extraction headroom before each partition. E checks for 60 GiB free between RPMs and retains its SQLite database. Friday reporting uses completed measurements only.

## 2. Native host tonight · Tier 2 · dedicated pkg lock

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree/workspace/temp
  d=$(mktemp -d "$PWD/pm0013-get.XXXXXX")
  pin=9047570ba80a43965d92ce90b8b38ffb8664e946
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 150 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013a/run.sh.txt" -o "$d/run"
  printf '%s  %s\n' fca915876ba930af427c82b62016effa99c80ea12082059dbc22865742c24f42 "$d/run" | sha256sum -c -
  bash "$d/run" "$pin" 152a1274626f1cba04662ef9d88a6aefdae4133faabb522a8fc3c2968711ff68 pkg
)
```

Use a separate foreground or screen terminal with an active P4 ticket and normal local GBS credentials. One package build at a time, six allowed cores, one GBS thread, nice 19, idle I/O, private buildroots. Ranking reads the new Official RPMs independently. Friday's stop is **09:30 CST (01:30 UTC), 27 November**. The worker checks the 60 GiB floor during its own GBS process and before builds. Existing D-018 lane admission requires 74 GiB free and 28 GiB available RAM at lane start. Results accumulate across completed packages in this run. Network and disk use depend on sources, RPMs and buildroots. Runtime ranges from minutes per small package to hours. The kernel job retains priority.

## 3. Native host after the kernel · full A32 roster

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree/workspace/temp
  d=$(mktemp -d "$PWD/pm0013-get.XXXXXX")
  pin=9047570ba80a43965d92ce90b8b38ffb8664e946
  read -r -p "Paste the PILOT_RECEIPT line from this B+C+E run: " tag receipt digest
  test "$tag" = PILOT_RECEIPT
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 150 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013a/run.sh.txt" -o "$d/run"
  printf '%s  %s\n' fca915876ba930af427c82b62016effa99c80ea12082059dbc22865742c24f42 "$d/run" | sha256sum -c -
  bash "$d/run" "$pin" 152a1274626f1cba04662ef9d88a6aefdae4133faabb522a8fc3c2968711ff68 roster "$receipt" "$digest"
)
```

Paste the complete `PILOT_RECEIPT` line when prompted. The command validates the hash, job identity and gates before trying the queue and shared locks without waiting. Run after the kernel has released them. Allow several hours, one low-priority worker, sequential full partition extractions and on-demand matching debuginfo downloads. The result lists every measured ELF with any mapped A32 in `.text`, including mixed-state files and kernel modules. It also exports unmapped and unowned rows. A separate-debug join requires the build ID, section address and size. Estimates in the image-wide executable-byte totals stay separate from measured mapping-symbol bytes. The installed E5 join uses exact path and payload hash on the new Official image when the original E results are present.

All three commands print the exact native run directory and section status. Full tables remain there. Part 1 and the SHA-256 of the uncompressed tar are printed automatically. For further parts use the emitted `NEXT_PAGE` command with successive page numbers. `B 2` means host qualification still needs evidence; inspect `pilot.json`. `C 2` can mean extraction succeeded and a board sample is missing; inspect the four partition rows. An unavailable reference or an incomplete E scan keeps the relevant conclusion open.

## Decisions and evidence · 26 November

**New pair.** PM accepted Official 37777148 and Custom 37777264 for the next board comparison. All 5,880 Product source/VCS rows match, 138 RPMs are byte-identical, and 5,742 differ. The tool verdict remains REVIEW. Submitted shelf and Base-list copies are unavailable, the published Product versions are 0825.10/0825.20, and the publication IDs are 19437567/19437655. Both publish the same build.conf SHA-256 beginning `98690f23`. All six kernel artifact hashes and both kernel build IDs changed relative to the prior pair. The sent kernel table remains tied to 37736448/37736427. [Verified native evidence](../../artifacts/evidence/native-run-r0012z-pilot-pair-reader-20261126.txt) · [Weekly byte tables](../../reports/weekly/2026-11-27/draft-data.md)

**B · AVControl.** The third column's reference comes from the retained `baseline` GBS lane. The production reference for ABI and LTO comes from the O1 Official AVControl ELF and matching debug evidence. The prior run passed the initial smoke and T3 in both treatments. T8 is N/A for this package. T1, T2, T4, T5, T6 and T7 still require the new readback.

| Gate | Evidence the rerun uses |
|---|---|
| T1 | Lane LLVM 22.1.8 reads bitcode from the executed link. The earlier package failure used host LLVM 18.1.3. Compare Official DWARF/link and spec evidence with the default lane's effective LTO option. If Official links LTO and default drops it, restore the Official final link policy and repeat the default lane before making a like-for-like claim. |
| T2 | Mapping symbols on the output or exact matching debug file. Linked objects and linker placement must account for the final bytes. Earlier uncovered bytes were 441,362 in default and 179,660 in package. |
| T4 | Versioned dynamic symbols with type, binding and size, NEEDED, SONAME and dynamic flags against the shipped Official ELF. This fallback does not provide DWARF type equivalence. |
| T5 | Spec test stage plus source and generated CMake/CTest registration. N/A requires evidence. |
| T6 | Root loader dependency resolution, eager relocation probe and disassembly of direct interworking branches. Signed application start on the target remains a separate board gate. |
| T7 | Executed link inputs, retained compiler CUs and their compilation directories. The prior checker lost the default lane at the non-LTO branch and used basename joins; the replacement checks normalized paths and ambiguous matches and excludes CMake compiler identification probes. |
| Output | Per-lane file size, .text, ARM/Thumb/data/unknown, and T1–T8. A PASS receipt requires both treatment lanes, explicit config/IT delivery and evidenced gates. |

**C · Reader.** The retained kernel's algorithm 4 dispatch and raw inflate init identify the decoder. The two old vendor x86_64 1.8.10 RPMs have published hashes beginning `cec29e50` and `19878237`; each new snapshot is also queried. For each partition the evidence consists of the input hash, fsck, full extraction, entry count against dump, sample hashes and ARM census. Two Official prd board hashes remain due from a matching Official visit; the optional `PM12Z_OFFICIAL_PRD_SHA256SUMS` input accepts its versioned readout under the native workspace. If the vendor executable cannot run, its dependency/version diagnostics precede a separately reviewed decoder port against upstream 1.9.4. [Source and publication evidence](../../artifacts/evidence/native-run-r0012z-pilot-pair-reader-20261126.txt)

**E · Published RPMs.** E1 attributes compiler markers and reports corroborating DWARF where available; a VCS observation alone cannot prove membership of an unpublished shelf. E2 retains observed CU options and marks omissions. E3 separates final-link signatures from other LTO evidence. E4 reports executable/readonly relocation targets and page upper bounds. E5 is a static import/export screen: publication scope includes uninstalled RPMs, and runtime lookup and inline semantics require separate evidence. E6 measures relative relocation density, packing estimates and actual linker tag emission. Packed records do not eliminate relocation writes to writable pages. [Optimization tracks and outstanding measurements](../../reports/weekly/2026-11-27/draft-data.md)

**Package sequence.** Rank by new Official .text within N5, N4 and each experiment. N5 covers the remaining 30 candidate names; a blanket libgcrypt override is withheld pending per-file exceptions. N4 selects up to ten ranked candidates and retains both on/off delivery evidence plus the GCC-reference ABI result and missing outputs. R4-50/R5 use the four staged package recipes and retain executed linker arguments. Public source/VCS and the retained November shelf manifest support a local reconstruction; exact new QB submission inputs remain unproved. Unranked packages, absent source, missing driver evidence, ABI differences and stops stay visible. Stability and performance still require board measurements. R2, R3, R6 and strict `-z text` remain gated.

**Validation.** Python 3.10.12 compiled the staged Python inputs. Local fixtures checked all 25 file pins, the review-packet hash, ELF/relocation parsing, ambiguous CU matches, invalid pilot receipts, and lane-specific staged macros. The native commands, vendor decoder, matched build-root loader and tonight's package builds await Claude review and operator execution. Native evidence archived verbatim, SHA-256 `7f052f1b43d0d9baaf573b4eb25abd6ea6d6e78e29caf3dd050f4aa0073df5b0`.
