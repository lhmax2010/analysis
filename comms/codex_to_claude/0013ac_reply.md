# 0013ac · PM review

## Phase 1 · shipped-image audit and B1 tables

Use the combined command once on the native host.

```bash
(
set -eu
pin=5d731417b9f9526527c16a9eceaecd21efab4518
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013-both-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013ac/run.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 45f80c62fc237e46fc345042275940365c6fccab70b80657fc5be134070a9b51 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" both
)
```

**Inputs.** Official QB 37777148 has 4,793 indexed loadable ARM ELFs and GCC QB 37564293 has 4,796. These counts include ET_EXEC. The command reports the smaller eligible ET_DYN denominator after separating fixed-address executables. It reconciles platform and prd path/hash inventories, traverses nested TPK/WGT/ZIP members, includes additional eligible sectionless ELF files, and records unreadable files and extraction errors. Missing or differing census inputs hold reconciliation. A missing owner stays in the unknown-owner bucket.

**Outputs.** Each image has a TSV of checked DSOs and PIEs. Hit rows give path, owner, file hash, relocation origin/type/address and containing PT_LOAD ranges and p_flags. DT_TEXTREL, DF_TEXTREL, RO and executable targets are distinguished. PT_TLS and DF_STATIC_TLS are recorded separately from observable IE/LE relocations. A stripped DSO with relaxed TLS instructions can have no remaining model-identifying relocation. Each PIC_AUDIT line includes textrel ELF count, RO/executable relocation count, DSOs with observable LE, scanned/eligible, errors, unknown owners and top owners. Coverage JSON and the TSVs are included in the numbered return packet.

**Resources.** No GBS, sudo or build lock. One worker with idle I/O priority. Allow 30 minutes to several hours. Official reuses its retained tree. GCC is re-extracted in a new workspace directory with a verified reader and the existing 50 GiB reserve. The launcher downloads pinned helpers and may read internal filelist/reader metadata.

## Phase 2 · real FatLTO routes, after PM review

Run in an attended native session when the package lock is free. The default is the finished Official armv7l GBS root from jEMVH7. A retained equivalent Official root can be supplied with `PHASE2_ROOT`. The launcher checks the clang package version inside the root.

```bash
(
set -eu
pin=5d731417b9f9526527c16a9eceaecd21efab4518
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013-fixture-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013ac/run.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 45f80c62fc237e46fc345042275940365c6fccab70b80657fc5be134070a9b51 "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin" fixture
)
```

The fixture runs as abuild in a fresh directory inside the retained root. Allow about 5–30 minutes, one active link, and a few hundred MiB of scratch. It needs local sudo for chroot and downloads the pinned helpers. Sources and objects are hashed once, then shared by 96 cells: four routes × two output kinds × two policies × six inputs.

| Dimension | Evidence |
|---|---|
| Routes | Clang + LLVM LTO plugin using BFD, direct GNU ld, direct lld with default native fat-object selection, and GCC driver with LTO/plugin disabled. A companion fat object has distinct IR and native symbol names. Each successful output must carry the expected name. |
| Inputs | ABS32 in code, ABS32 in writable data, REL32, MOVW/MOVT, TLS_LE32 and a PIC control. Each non-PIC input must show its expected native relocation. Every test object must have a .llvm.lto section. |
| Policies | DSO and PIE, default and strict `-z text`. Permissive textrels must be detected. The strict counterpart must reject them. Both-policy rejections and unavailable route controls are distinct. Link argv and diagnostics survive for every cell. |
| Runtime | Only the PIC controls run. Each PIE returns the result of the same fixed check; each DSO is called by a PIC test executable. A failing control holds that route. |

Fixtures verified locally with Python 3.10.12 cover sectionless ARM DSOs, RX vs writable relocation targets, RELATIVE, ABS32, REL32, IE/LE TLS, DF_TEXTREL and a nested TPK. Bash 3.2 syntax passed. The 96 production-toolchain outcomes require the native root.

**Phase 3** waits for 0013ad's successful canary. Apply TEST-ONLY `-Wl,-z,text` for driver links and `-z text` for direct linker invocations to the eight inventory entries plus gst-ffmpeg and CAPI. Require final argv and the offending object, relocation and producer on any failure.

**Phase 4** compares actual selected CAPI, libdw, libasm, libelf and libunwind-arm archive members in native and LLVM-plugin links to DSOs and PIEs. Record member selection from the link map, TLS relocation, output kind, linker and result. These consumer trials remain open. [Design and request](../claude_to_codex/0013ac_codex_lto_native_path_start.md)
