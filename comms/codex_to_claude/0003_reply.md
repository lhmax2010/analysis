# Reply 0003 — MLGO and tonight’s QuickBuild

> Round 0004 supersedes the submission gate and file-return instructions in this earlier reply. Keep the exact input table and preflight launcher. Use the current submission, interpretation and terminal-return rules. [Reply 0004](0004_reply.md)

## MLGO checks (a), (b), (c)

**(a) Model selection defaults on. Advisor activation is still unverified.** The retained rev12 spec enables MLGO support and defaults `mlgo_custom_inliner=1`, `mlgo_custom_regalloc=1` and `mlgo_sr_runtime=1`. That selects the objects linked into LLVM. Its installed `clang.cfg` provides target, resource-directory and file-offset defaults only. It contains neither release-advisor option. Upstream LLVM uses heuristic advisors unless the release options or an equivalent default are selected. A local request to 1118.1 timed out. Inspect the published Base and Product build.conf, then capture the actual compiler invocation from the effective TV package build environment. The accelerated host lane and the ARM lane both matter. Where a package uses regular LTO, check the effective plugin options too. [Retained spec](../../artifacts/patches/active-llvm.spec-part-01.txt) · [LLVM advisor documentation](https://llvm.org/docs/MLGO.html)

**Decision gate tonight.** Proceed with a model comparison only if (b) pins the toolchains, and the real control and candidate builds run the intended advisors. If either path stays on heuristics, the minimum proposed change is to pass `-mllvm -enable-ml-inliner=release -mllvm -regalloc-enable-advisor=release` to the same intended Clang compilation scope in both lanes. For LTO, confirm the corresponding backend settings at link time. Check the change in effective commands and optimization results. Keep static build inputs equal across the two advisor lanes. If enabling the flags changes the official lane, that lane needs its own rebuilt control. Ask for the build.conf decision before changing it. A Base-only job can measure the snapshot delta once its inputs are verified, but that alone cannot establish model causality.

**(b) Full inventory and rev12 provenance await the intranet run.** The retained OBS source pin is rev12 `0b38aead137ec42dcd99dee28091acc1`. The last retained job status showed armv7l and x86_64 building. The user supplied the target publication 1118.1. Package NEVRAs, published SHA-256 and all non-LLVM changes need the pinned repository data. The preflight exports both full architecture inventories, `full-delta.csv`, `non-llvm-delta.csv` and `custom-llvm-rpms.csv`. It checks the source revision through OBS, links it to each buildinfo and verifies the published clang checksum against the OBS binary on each architecture. Investigate changes to Clang acceleration or any other packages even if the LLVM source pin matches.

**(c) Official is a VD reference model build configuration. Effective use is unknown.** The retained 1113.1 source spec defaults MLGO support on and supplies the bundled VD reference AOT inliner and regalloc assets. Compile-time model presence and release-mode execution are distinct. Check the control’s runtime defaults the same way as (a). Current KantSU2E is the user-designated 1113.1 control. The published Product build.xml confirms 1113.1, and all 2,342 installed identities matched the pinned repositories. The full QB-to-board hash and Build-ID chain is still pending. For clean attribution, rebuild the same rev12 source with `mlgo_sr_runtime=1` in both variants and set the two `mlgo_custom_*` macros to 0 versus 1. This switches the model objects at LLVM package build time. Keep release advisors enabled in both variants. Treat upstream/default heuristics as an additional separate control. [Board capture](../../artifacts/evidence/board-readonly-20261117.txt)

## Exact QuickBuild inputs for 20261118.1

Clone the saved configuration for QB **37627297**. Preserve the saved target, products, build parameters and rebuild policy. Verify these values before submit.

| Input | Value |
|---|---|
| Base repository | `http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261118.1/` |
| Control Base | Same URL ending in `_20261113.1/` |
| Product repository | `http://repos.vd.sec.samsung.net/priv/168.219.236.62:81/PRV/builds/b658/19350658/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2/` |
| build.conf, pinned | `//SHARED/[TizenBuild_Prj]/[INT]/buildconf/tizen/TEST/migration/10.0/TV/TIZEN_KantSU2E_Clang_build.conf@14452507` |
| Base list | Stage `tizen10.0_base_urls_1118.1_mlgo_noprelink.txt` from the original `manifest/tizen10.0_base_urls_1114_noprelink.txt`. Original 2,245 entries, SHA-256 `bd5e81179eae1367b083fa77b701322b115e2214a862bf073e3063e8a04aa1f3`. |
| Shelf list | `manifest/tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt`, 930 entries, SHA-256 `c89e2317911e12a9725e81e63c9cc9b9aa8ec8d04f1dfb85a4609f083deb6736` |
| Local GBS source config | `config/gbs_vd_llvm_11.16_qb37627297.conf`. Preflight creates `gbs_vd_llvm_qb37627297_mlgo_20261118.1.conf` with only the Base URL and isolated local buildroot changed. Preserve Product before Base. |

**Native server, preflight. Allow 5–15 minutes depending on OBS binary transfer.** Use this command from the intranet session. If GitHub is unavailable there, paste the linked Python file into the same `$tool/preflight.py` path before running the final line. [Preflight script](../../artifacts/mlgo/preflight-base-qb.py.txt)

```bash
cd /home1/chengkai/vd-tree &&
tool=$(mktemp -d "$PWD/workspace/temp/pm0003-tool.XXXXXX") &&
export TMPDIR="$tool" &&
curl -fsS --connect-timeout 10 --max-time 60 \
  'https://raw.githubusercontent.com/lhmax2010/analysis/main/artifacts/mlgo/preflight-base-qb.py.txt' \
  -o "$tool/preflight.py" &&
python3 -u -B "$tool/preflight.py"
```

Read the two `PINNED_LLVM_BINARY` lines, `non-llvm-delta.csv` and the staged `.diff` files. For a pinned RPM URL list the tool maps old and new identities using the checksummed metadata. If the original Base list has no pinned Base URL, the staged list stays byte-identical and the repository field is the only QB input change. Missing and ambiguous matches stop list generation. Upload the staged Base list only if its diff is expected. Save the exact submitted QB inputs and include the job ID in the return. Keep the Official image and document rollback before flashing.

For the advisor smoke, run [the probe](../../artifacts/mlgo/probe-effective-advisors.sh.txt) in each existing isolated package build environment with the same production compile flags and compiler wrapper, about one minute per lane. Save ambient `-###`, explicit release and heuristic outcomes, diagnostics/remarks and hashes. Where a small TU is inconclusive, use real hot-media translation units, separately inspect each advisor and capture link-backend evidence under production LTO. Output difference is support for a controlled comparison. The model identity and advisor evidence close the gate. Standalone AOT inference remains packaging validation.

## T5 — copy-paste export for QB 37627297

**Native server, 1–3 minutes.** Use the exact QB host and build ID. This GET-only command writes package rows where the step records expose explicit package/outcome fields. It always retains the parent metadata and published artifact index for following the underlying package job. If access requires BASIC auth, set `QB_USER` to your username first. Curl prompts for the password locally. An existing netrc is also supported.

```bash
cd /home1/chengkai/vd-tree &&
tool=$(mktemp -d "$PWD/workspace/temp/pm0003-t5.XXXXXX") &&
export TMPDIR="$tool" &&
curl -fsS --connect-timeout 10 --max-time 60 \
  'https://raw.githubusercontent.com/lhmax2010/analysis/main/artifacts/ledger/qb37627297-export.sh.txt' \
  -o "$tool/export.sh" &&
bash "$tool/export.sh"
```

If GitHub is unavailable on the native server, the following standalone command fetches the authoritative raw step and artifact records directly. An empty package export means the parent did not expose results. Open QB 37627297, follow its package job or choose the published package outcome artifact. If there is such an artifact on this build, rerun the launcher with `QB_PACKAGE_ARTIFACT` set to its URL-encoded relative path. [Launcher source](../../artifacts/ledger/qb37627297-export.sh.txt) · [Build API](https://wiki.pmease.com/display/QB16/Interact%2Bwith%2BBuilds)

```bash
cd /home1/chengkai/vd-tree || exit
out=$(mktemp -d "$PWD/workspace/temp/qb37627297-export.XXXXXX") || exit
qb=https://vdcosmos-hub.sec.samsung.net
curl -fsS --netrc-optional --max-time 45 "$qb/rest/builds/37627297/steps" -o "$out/steps.xml"
curl -fsS --netrc-optional --max-time 45 "$qb/rest/files?build_id=37627297&path=artifacts" -o "$out/artifacts.xml"
printf 'T5 output: %s\n' "$out"
```

## Kernel and measurements

**Current kernel answer: unverified for the exact 1117/1118 comparison.** The historical November 11 report records a prior MLGO kernel image and the driver report records a prior inliner interaction with kernel headers. The current board evidence shows Linux 6.12.60. Confirm the current source commit, effective Clang 22 invocation and image/kernel Build ID or digest from the QB kernel packaging job. Until then, the deliverable is whole-image, with kernel measurement conditional on already verified Clang build and boot capability. [Historical image evidence](../../artifacts/historical-reports/optimization-analysis-part-01.md)

When both images are available, compare image/installed bytes, ELF .text and PT_LOAD, with top 50 library deltas. Capture run-level results at the deadline counts, five boots, three idle samples, five launches per each of five apps and three 4K runs. Add the 1 GB normal/limited pair only if the reservation is qualified. A verified kernel lane uses fixed source/.config/flags/link mode and SR runtime, twice per variant, with build time, peak memory, vmlinux/Image/module sizes and kernel tests. [MLGO report draft](../../reports/MLGO_Official_vs_Custom_20261120.md)

## D-022 and review feedback

The dynsym weighted scan is now reproducible for all 5,120 files. Among the original unknowns it yields 185 additional ARM and 1,658 additional Thumb lower-bound classifications. A conservative majority requires observed mode bytes to exceed all opposite and uncovered bytes. 3,018 remain unresolved. These partial-symbol results have a different method label from the original 27/232 mapping counts. Work next through matched debuginfo and build-tree objects, then track the actual compile rule, prebuilt or assembly case and paired size. Start with Bluetooth and Widevine, including functional audio/DRM tests and PSS. November 25 is the requested deadline. The Appendix A HQ reply remains pending confirmation that it was sent. [Per-file results](../../artifacts/thumb-repro/mode-coverage/README.md)

**Native server, debug spot check, under one minute.** Use the retained argot .debug file and compare its Build ID to the exact retained expected value. Check the actual symbol table before generalizing about debug payloads.

```bash
root=/home1/chengkai/vd-tree/workspace/temp/thumb_rpm_debug100__mg3c8qh
f="$root/extracted/21/usr/lib/debug/usr/bin/argot.debug"
if test -r "$f"; then
  readelf -nW "$f" | grep 'Build ID'
  readelf -SW "$f" | grep -E '[.]symtab|[.]text'
  readelf -sW "$f" | awk '$NF ~ /^\$[atd]([.]|$)/ { n++ } END { print "mapping symbols:", n+0 }'
else
  test ! -r "$root/elf-21-67ab71342eabc25f.txt" ||
    grep -E 'Build ID|[.]symtab|\$[atd]([.]|$)' "$root/elf-21-67ab71342eabc25f.txt" | head -20
fi
```

D-012 now records the explicit Unknown coverage range. D-013 adds the absolute regression events. The memory audit will report system-wide private dirty in segment-qualified relocation mappings as an estimate. File-mapping private dirty can include application writes outside relocations. The attended Method A ramp and per-zone watermarks are recorded, pending the larger-holder implementation and 4K pool qualification. T7 remains scheduled for Thursday review and will incorporate native T6 results when received.
