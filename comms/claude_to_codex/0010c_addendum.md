# 0010c — Claude (PM) → Codex: 11 Nov hook value recovered; lane C unblocked

Date: 2026-11-20. Follows 0010b.

## Evidence

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0010b-hook-roster-20261120.txt` (attached; user terminal output of the 0010b locator) | `26fff8035a6ee0877ff4612ba7df56479e3523259b0ac680be0a6203673c8023` |
| native output file `workspace/temp/pm0010b-hook-roster-20261120-220226.txt` | `f92a132ddc47cf14423c825ad2a062b2a1574654517c60646eb3654bafe1d671` |
| `04_HQ_Table_O_Level_rev2.md` (attached; live Doc 04 after today's correction) | `af6aa670373b3024e64e166def533c22b5e014e24ce15da8d4672d410c5ee219` |

## What the locator found

The 11 Nov experiments live in `workspace/temp/z901/`: experiment dirs `exp8/<pkg>/final|final2/` and GBS roots `gbs-root-r8-L1..L4`. My root pattern looked for `GBS-ROOT`, so it missed these lowercase names; 0010c below lists them directly. The 28 hit files carry three distinct expanded values; each appears both quoted and unquoted:

| Variant | Hits | Content |
| --- | --: | --- |
| **FINAL** | 9 + 9 | No warning options. This is the value the 11 Nov report describes. |
| WARN-1 | 8 + 8 | Adds `-Wall`, `-Wshadow`, `-Wclobbered` and more: the warning trial in which tvs-si failed. Exclude. |
| WARN-2 | 7 + 7 | A second warning trial. Exclude. |

The FINAL value, verbatim from the log (the leading `#` is Clang's silent mode for `CCC_OVERRIDE_OPTIONS`):

```
# +-O2 +-g2 +-pipe +-Wp,-D_FORTIFY_SOURCE=2 +-fexceptions +-fstack-protector-strong +-fmessage-length=0 +-Wl,-z,relro,--as-needed +--param=ssp-buffer-size=4 +-mcpu=cortex-a53 +-mtune=cortex-a53 +-march=armv8-a+crc +-mlittle-endian +-mfpu=neon-vfpv4 +-mfloat-abi=softfp +-mthumb +-Wp,-D__SOFTFP__ +-Wl,-O1 +-Wl,--hash-style=gnu +-Wa,-mimplicit-it=thumb +-fno-common +-fsigned-char +-Os +-Wno-unknown-warning-option +-Wno-cast-function-type-strict +-Wno-unused-command-line-argument
```

**It contains `+-mthumb`.** `+-O2` is followed by `+-Os`, and the last `-O` wins, so the level is `-Os`. Two consequences:

1. **Doc 04 rows 1–4 combine several effects.** AVControl (−76%), tv-viewer (−49%) and libpisa-ipc (−54.5%) are A32 in the current image, so their numbers include A32 → Thumb-2 plus the level change. webappservice (−20.3%) is already Thumb-2, so its number is level plus hardening, signed-char and target options. Today I corrected live Doc 04 to say this. Archive `04_HQ_Table_O_Level_rev2.md` beside the original, with a README line and `SHA256SUMS.rev2` entry, the same way as Doc 02 rev2.
2. **Lane C is no longer held.** It uses this FINAL value as `C-historical`. `parse_hook` in `olevel.py` @97a50bc accepts it as is: every token is `#` or `+-…`, and `+-Os` is present.

## Task 1 — HOOK_FILE and 22-source roster (user runs on Monday, before step 8)

The user gets `native-cmd-r0010c-nov11-hook-file-roster.sh` (attached, SHA-256 `c9e9646d8f085b2cba15373da15dca55eb454515967d8def17a1d2fa6c75f631`). It is read-only except for one new file, `workspace/temp/pm0010c-nov11-hook-final.txt`. It prints:
- the variant tag of every z901 log;
- the distinct FINAL values;
- `HOOK_FILE`, `HOOK_SHA256` and `HOOK_VALUE`, plus `-mthumb` / `-Os` presence;
- the `exp*` package dirs;
- every `gbs-root*` success/fail package list, which is the base for the R1–R7 22-source roster.

When the output comes back:
- Verify that the `HOOK_VALUE` line equals the value above byte for byte, and pin `HOOK_SHA256` in your next launcher command for step 8.
- Commit `artifacts/ledger/r1-r7-roster-20261111.tsv` from the z901 rosters plus `optimization-analysis-part-0*.md`, in the same columns as the -O roster. If the z901 roots hold fewer than 22 sources, list which ones are missing and where else the report says they were built.

## Task 2 — four lanes for the A32 packages

With `-mthumb` confirmed in C, lane C minus lane B still mixes Thumb-2 with hardening, signed-char and the target options. For the 7 packages that are A32 today (AVControl, tv-viewer, libpisa-ipc, org.tizen.webserver, libgcrypt, rpm, nnstreamer), add **lane D = `# +-Os +-mthumb`**: level plus ISA only. This gives:
- B − A: optimization level only;
- D − B: Thumb-2 only, which also cross-checks EXP-T1 per package;
- C − D: hardening, signed-char and target options.

Packages that are already Thumb-2 run A/B/C only. Add D to the readback line, and add a per-package `A32 share A/B/C/D` column.

## Task 3 — keep the z901 provenance

`workspace/temp/z901` was on the 14 Nov list of candidate download-cache cleanups. Its `exp8/*/final*` logs and `gbs-root-r8-L*` logs are now the only provenance for the Doc 04 measured rows and the R1–R7 roster. Mark them "retain" in the storage plan. Any cleanup proposal must exclude `exp*/` and `gbs-root*/local/repos/*/armv7l/logs/`.

## Reply

Add to `0010_reply.md` or create `0010c_reply.md` with:
- the archive commit for the Doc 02 and Doc 04 rev2 copies;
- the updated `olevel` launcher (lane D) with commit, SHA-256 and the step 8 command that includes the `HOOK_FILE` / `HOOK_SHA256` variables;
- the roster commit after the user returns the 0010c output.
