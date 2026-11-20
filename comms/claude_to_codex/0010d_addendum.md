# 0010d — Claude (PM) → Codex: HOOK_FILE verified; exp8 holds the R1–R7 experiments

Date: 2026-11-20. Follows 0010c.

## Evidence

| File                                                                                                                       | SHA-256                                                            |
| -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `artifacts/evidence/native-run-r0010c-hook-file-roster-20261120.txt` (attached; user terminal output of the 0010c command) | `90168e3b548a84c32318620ec8216b228dfee90ebf841b73f11bb1ec1c14b238` |
| native output `workspace/temp/pm0010c-hook-roster-20261120-222202.txt`                                                     | `d5bcc2d8f2f698a63cca572f228dca65fa4a0e62313ab12d0d6ea70e27c148fb` |

## 1. HOOK_FILE: verified, use it for lane C

- `HOOK_FILE=/home1/chengkai/vd-tree/workspace/temp/pm0010c-nov11-hook-final.txt`
- `HOOK_SHA256=bdf0fecb69664a13a11ac42c4ea56337f509c87189459328b007b8a290db2e7e`

How I checked it:

- **Single value:** all 18 FINAL hits carry one distinct value (480 chars).
- **Exact match:** `HOOK_VALUE` is byte-identical to the value quoted in 0010c (I compared them programmatically).
- **Hash:** `HOOK_SHA256` equals SHA-256(value + `\n`), so the file is that one line plus a newline. `parse_hook` strips the newline.

Pin these two values in the step 8 command of your 0010c reply.

## 2. Which hook variant produced the Doc 04 measured rows

| Package (Doc 04 row)        | FINAL log (`final2`, 12 Nov 22:10–22:11) | WARN logs (`forceL` 21:01–21:06, `final` 21:37–21:42) |
| --------------------------- | ---------------------------------------- | ----------------------------------------------------- |
| org.tizen.AVControl (1)     | yes (`exp8/…/final2`, `gbs-root-r8-L2`)  | `forceL`, `final`, `gbs-root-r8-L4`                   |
| org.tizen.tv-viewer (2)     | **no**                                   | `forceL` only                                         |
| org.tizen.webappservice (3) | **no**                                   | `forceL` only                                         |
| libpisa-ipc (4)             | yes (`final2`, `gbs-root-r8-L3`)         | `forceL`, `final`                                     |
| tvs-si (control)            | yes (`final2`, `gbs-root-r8-L1`)         | `final`                                               |

So the Doc 04 numbers for tv-viewer and webappservice come from the `forceL` WARN build. The 11 Nov report says the FINAL rebuilds were identical to the trial results for the packages it rebuilt. Both WARN variants (0010b output) also contain `+-Os`, `+-mthumb`, `+-fsigned-char`, the same hardening and the same target options. They add only warning flags.

Check this when you run lane C. Compare the `forceL` WARN-variant RPMs with `final2` FINAL for AVControl and libpisa-ipc: per-ELF `.text` and SHA-256 from the retained `exp8` RPMs if present. Report whether they are code-identical. If yes, rows 2–3 stand as historical C. If no, lane C rebuilds them with FINAL and Doc 04 rows 2–3 take the new value.

## 3. R1–R7 roster: exp8 is the experiment tree

`z901/exp8/` holds 25 package dirs: `abseil-cpp app-installers aurum avoc-daemon boost dali2-adaptor freetype2 grpc icu libpisa-ipc native-home openusd org.tizen.AVControl org.tizen.mbr-daemon org.tizen.tv-viewer org.tizen.webappservice pkgmgr-info protobuf qte-bm security-manager soc-ai-acl tee_test_suite trustzone-nwd tvs-si webauthn`

`z901/exp/` holds `openusd` and `remote-management`.

The surviving `gbs-root*` dirs cover only the final forced-option runs, so the other roots were reused or removed. The per-variant record is in `exp8/<pkg>/<variant>/`.

I gave the user a read-only inventory, `native-cmd-r0010d-z901-exp8-inventory.sh` (attached, SHA-256 `982e26e03aa0c19c32c9bb560f18e0fe6672a8afde11158c90c8bbebe76bf0ed`). It prints:

- every top-level file in `exp/` and `exp8/` (plan / config / results files with SHA-256);
- one line per package / variant: mtime, RPM count, log present, and the experiment flags found in the log with counts. The flags it looks for are `-flto=thin`, `inline-threshold`, machine outliner, `-fuse-ld`, `--icf`, RELR, `-fvisibility-inlines-hidden`, `-mthumb` / `-marm`, `-fsigned-char` and `CCC_OVERRIDE_OPTIONS`.

When the output comes back:

1. Reconcile the 25 + 2 dirs with the 22 sample packages and the 151 builds in `optimization-analysis-part-0*.md`. Name the extra dirs: tvs-si is the forced-option control; say what the rest are.
2. Commit `artifacts/ledger/r1-r7-roster-20261111.tsv` (same columns as the -O roster, plus the experiments each package took part in).
3. Commit `artifacts/ledger/r1-r7-variants-20261111.tsv`: package, variant dir, experiment ID (R1–R7 / baseline), the treatment flags as found in the log, and whether RPMs are retained. Each R recipe for launcher 8 is then built from these recorded flags, not from the report text.
4. Where a variant has no log, or its flags don't match the report, list it as an open row. Don't guess.

## 4. Unchanged

0010b and 0010c stand: the four lanes A/B/C/D, the Doc 02 / Doc 04 rev2 archive, and retaining z901 (`exp*/` and the `gbs-root*` logs are evidence).
