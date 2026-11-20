# PM → Codex, round 0009: linker probe proves the silent case, PERF layout, kernel ISA correction

Evidence file (byte-identical copy in ~/Downloads):
`native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt`, 363 lines,
sha256 `803581c1ec1930561d22dea4806a8fd5cdf718285736d80fa4912d42b2f83321`.

What the transcript contains:

| Lines | Content | Result |
|---|---|---|
| 1–51 | **The user's USB image procedure** | — |
| 54–68 | `perf-relocations` | **BLOCKED** |
| 69–160 | `gbs-native-textrel` | **COMPLETE** |
| 161–286 | `qb-forensics config` + `helpers` | done |
| 287–362 | `native-build-readback kernel-isa` + `modules` | done |

## 1. How the PERF bundle becomes a flashable image (operator procedure, record in docs)

1. Extract the PERF `.tar.gz` **directly into a folder named `updateSU2E`**. The archive has **no inner tar**: its members are the flat files listed at L14–40, including `platform.img`, `do_not_use.img`, `systemrw.img`, `factory_peq.img`, `uImage`, `zImage`, `dtb.bin`, `dtb_RW.bin` and `partition.txt`.
2. Rename `do_not_use.img` to `data.img`.
3. Delete `dtb.bin`.
4. Rename `dtb_RW.bin` to `dtb.bin`.
5. Copy the folder to the USB root and flash: BOOST, then `~`, then the mmc menu, then `a`.

Deliverables for this procedure:

**(a) Fix `perf-relocations`.** `PERF_AUDIT_BLOCKED no named inner image archive in PERF bundle`. Your parser expected a nested tar. Read the partition images straight from the outer `.tar.gz` members. Use `partition.txt` (and `partition_8G.txt`) for the image-to-mountpoint mapping; `do_not_use.img` is the data partition. Keep everything else:
- read-only `debugfs`;
- `simg2img` when sparse;
- explicit scope and INCOMPLETE reporting.

**(b) New `perf-usb-prep` launcher.** It builds `workspace/usb/<QB_ID>/updateSU2E/` from a captured bundle:
1. verify the archive sha256;
2. extract;
3. apply the 3 renames;
4. print a manifest (name, size, sha256) and the free space.

It must not flash anything; the operator copies the folder to the USB. It must refuse to overwrite an existing folder. We will use it for both matched-rebuild images.

## 2. GNU ld probe: the native-path silent case is PROVEN

Toolchain: Tizen GBS, `GNU ld (GNU Binutils) 2.43`, `binutils-2.43-3.49.armv7l`, ld sha `2b5cb608…`.

| input relocation | shared, default | PIE, default | `-z text` |
|---|---|---|---|
| `R_ARM_ABS32` in `.text` | **rc=0, DT_TEXTREL + FLAGS TEXTREL**, dynamic `R_ARM_ABS32` | **rc=0, TEXTREL** | rejected: "read-only segment has dynamic relocations" |
| `R_ARM_ABS32` in `.data` (control) | rc=0, no TEXTREL | rc=0, no TEXTREL | rc=0 |
| `R_ARM_REL32` | rejected ("recompile with -fPIC") | rejected | — |
| `R_ARM_MOVW_ABS_NC`/`MOVT_ABS` | rejected | rejected | — |
| `R_ARM_TLS_LE32` | rejected ("not permitted in shared object") | rc=0 (valid for PIE) | — |

The production configs searched (Product `98690f23…`, Base `b5e6d8e1…`) have **0 literal `-z text`/`notext`** occurrences.

Conclusions to write into `hq/PIC_FatLTO_Dual_Path_Design.md`. These are verified facts; state them plainly:
- With the Tizen GNU ld default, a non-PIC absolute data reference in code links silently into a shared object or PIE and produces `TEXTREL`. `-z text` turns it into a link error.
- REL32 and absolute MOVW/MOVT are rejected for shared and PIE outputs. Local-exec TLS is rejected for shared objects and accepted for PIE.
- The current production link flags do not set `-z text`.

So proposal item 2, `-z text` in the LLVM build.conf, closes exactly the one native case the default leaves open. Tighten the design text accordingly, and add the fixture to the verification table as "done" evidence.

Then rerun the fixed image audit (1a) for the baseline count. The design can go to HQ before the baseline returns, because the baseline is verification step 1. Tell me if you disagree.

## 3. QB config: build.conf difference confirmed; the Friday report must state it

- Official QB: `TIZEN_KantSU2E_Clang_build.conf@14452507`.
- Customized QB: `@14431365`.
- The only difference is `%lto_uncompatible_pkgs`: Customized **adds** ci-module, liballshare-core, nagsam-mw, org.tizen.tv.swu and ug-hbbtv-efl. So in the Customized image those packages were built **without LTO**. That accounts for the four positive `.text` growths (swu +12.7%, liballshare-core +11.0%, nagsam-mw +1.6%, ug-hbbtv-efl).

Update the report:
- The **user-space** `.text` growth of the old pair comes from a **build.conf LTO-exclusion difference, not from the compiler or model**.
- The remaining 5 changed packages (chromium-efl, connectivity-common-daemon, key-manager-ta, ABC-test-apps, gst-ffmpeg) have zero or tiny size changes. List them as unattributed: candidates are Base dependencies and non-determinism.
- The kernel comparison is unaffected: the GBS replay used one published build.conf for both lanes.
- Remove the stale sentence in 0008_reply §4: "The operator attributes the old nine-package delta to the separate build dates."
- The matched rebuild pins `@14452507` for both lanes.

## 4. clang-force-options: the Thumb fix vehicle exists. Design the experiment on it

`clang-force-options-1.0.0-1.1` (from `clang-contrib`, in both Bases) works like this:
- Its `%post` makes `/usr/bin` writable and appends `macros.clang_force` to `tizen_macros`.
- `%clang_force_incompatible`, run from `%__spec_build_pre`, appends a marked block with `%clang_force_options` to `clang.cfg`/`clang++.cfg`.
- The block is removed in `%__spec_build_post`.
- It honours `%clang_force_incompatible_pkgs` and the `%gcc_warning_*_pkgs` blacklists.
- Default: `%{optflags} -Wl,-z,relro,--as-needed -Wl,-O1 -Wl,--hash-style=gnu`.

Note that config-file options precede command-line options. So unlike the GCC wrapper, which appends, an explicit package `-marm` still wins. This is option (a) semantics.

Experiment design, one change per experiment:

| | EXP-T1 (Thumb) | EXP-Z1 (strict link, later) |
|---|---|---|
| build.conf change | `Preinstall`/`RunScripts: clang-force-options` + `%clang_force_options -mthumb` | `%clang_force_options -Wl,-z,text` |
| other flags | none; do not inherit the full `%{optflags}` default | none |
| Base | Official 1113.1 | Official 1113.1 |
| Product | the matched rebuild | the matched rebuild |

**Kernel risk.** SAVED_ARGV_ISA shows no `-marm`/`-mthumb` in the retained Clang kernel argv (`{(): 7100}`). If the perf kernel really has no explicit `-marm`, a forced `-mthumb` would change the kernel ISA without `CONFIG_THUMB2_KERNEL`. Before EXP-T1:
- prove the perf kernel's actual ISA flags (see §5);
- exempt the kernel and every external-module package via `%clang_force_incompatible_pkgs`.

Measure:
- the ARM-predominant count and each file's `$a`/`$t` share, with `image_mode_scan`;
- `.text` per package and image totals;
- build failures;
- on KantSU2E: boot, the playback smoke and PSS of the top media processes.

Give me the exact build.conf lines and a GBS 3-package pilot launcher (deviced, gst-plugins-dash, inference-engine-tflite) using a temp copy of the build.conf **before** any QB.

## 5. Kernel ISA: my earlier conclusion was based on the wrong .config. Correct it

- The 1,884 `-marm` lines are **GCC** compiles at about 1083s+ / 1172s+ (`gcc -Wp,-MMD … -mcpu=cortex-a15 -msoft-float -marm`). They come from the **SERET-UL** kernel builds (`vd_src/SERET-UL/build/KANTSU2E/{debug,release}/vdlinux`), not the perf Clang kernel. So the `# CONFIG_THUMB2_KERNEL is not set` lines also come from SERET-UL configs.
- `PERF_CONFIG_NOT_FOUND`: the perf kernel `.config` has not been located.
- The 302 `-mthumb` lines are rpm `CFLAGS=` shell traces, not compiles.

Deliverables:
- **(a) Locate the perf kernel `.config`** in the retained GBS BUILD tree and read `CONFIG_THUMB2_KERNEL`.
- **(b) Measure the ISA directly.** Run `image_mode_scan` (or a mapping-symbol count) on the retained GBS perf `vmlinux` ELF in each lane (`.../KANTSU2E/image/perf/vmlinux`). The `$a`/`$t` share is the answer, independent of argv truncation.
- **(c) Check whether the saved argv is truncated** before the ISA flags, which would explain the empty ISA set.
- **(d) Scope rule.** SERET-UL is built with **GCC** inside `tztv-kernel`. Record it as a GCC-built component, and say whether it falls under the scope rule ("only RPMs that can only be built with GNU GCC may stay off Clang"), or whether it is a migration candidate.

Correct the 0007 ledger and the report text wherever they say the perf kernel `-marm` comes from `CONFIG_THUMB2_KERNEL`.

## 6. Modules

MODULE_SCOPE 44 owners / 60 rows: 58 TEXT_CHANGED, 2 TEXT_IDENTICAL (`tztv-proidiom-perf`, one `wifi-drivers-RTK-rtl8822EU-perf`). Put this in the report.

## Deliverables

- Commit the evidence.
- The fixed `perf-relocations`, then `perf-usb-prep`, as pinned launchers.
- The HQ design updated with §2.
- Report corrections from §3, §5 and §6.
- The EXP-T1 design with the 3-package GBS pilot launcher.
- The kernel ISA launcher.