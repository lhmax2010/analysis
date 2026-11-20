# KantSU2E board day for the Official and Customized MLGO comparison

Claude review is pending. Run one numbered step at a time. Paste its compact terminal output and any requested observations. Wait for Claude or Codex to confirm the gate before advancing. Apply that pause to every individual cold boot and playback trial. Record board serial, QB IDs and measurement lane with every batch.

## Independent review of the proposed order

| Proposed step | Correction |
| --- | --- |
| 1. Measure Official first | Establish the currently running image's identity and have a verified rollback image ready before starting. Preserve each result on the native host as it is collected. Five software reboots or five reads of uptime cannot establish five cold boots. |
| 2. Prepare a candidate USB and keep Official available | Verify both prepared directories and their USB copies before flashing either. A locally calculated digest checks byte consistency. Provenance comes from the fixed QB artifact listing and, when available, its independently published digest. A Product RPM repository may contain no full flash image. |
| 3. Enter BOOST and flash | Separate entering BOOST from selecting `a`. Verify the USB, exact directory name, menu text and recovery access first. The key sequence below is the operator's supplied procedure. The completion prompt and error recovery need confirmation on this board. |
| 4. Identify and measure the candidate | Kernel version, package NEVRA and package count are sanity checks and may be shared by both builds. Require a build stamp, running kernel fingerprint or equivalent discriminator tied to the expected image. Reuse the exact benchmark binary and test clip. |
| 5. Roll back immediately on any failure | Recover a failed build or stability regression with a verified Official image when the board is idle and BOOST is available. A bad sample or missing counter only invalidates that result. An uncertain flash state requires recovery guidance before any interruption. Confirm the running Official identity after rollback. |

## Native commands

### Capture and prepare a flash bundle

Capture each completed QB immediately using the [retention launcher](../comms/codex_to_claude/0007_reply.md#1-customized-availability-and-immediate-retention) and retain artifact-to-board identity. The old Official QB 37627297 returned HTTP 404. Customized QB 37654439 is already captured. Secure the reviewed replacement pair or a verified Official rollback image before the first flash. [QuickBuild capture](../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt) [Operator USB procedure](../artifacts/evidence/native-run-r0008-ldprobe-forensics-usbmethod-20261120.txt#L1)

The PERF gzip archive holds flat files. Its companion manifest describes a loop image, and the operator's archive listing establishes the delivered shape. Run the [PERF USB preparation launcher](../comms/codex_to_claude/0009_reply.md#2-prepare-the-usb-directory) separately for each captured lane. It checks the archive digest, writes `workspace/usb/<QB_ID>/updateSU2E/` and prints `USB_PREP_READY`. The helper stages `do_not_use.img` as `data.img`, discards the original `dtb.bin` in scratch, and stages `dtb_RW.bin` as `dtb.bin`. The per-file checksum manifest sits beside the folder. Retain the full bundle, its hash and both prepared directories for the board run.

### Prepare and retain the board tools once

Before the measurement step, prepare a verified static ARM microbenchmark built in GBS. Put it in the verified tools directory as `microbench` with a matching `microbench.sha256` and record its GBS provenance. The current TV runner also has a host-compiler path and must be gated on the presence and verification of both files. The GBS benchmark binary is a board-day prerequisite.

Run on the native server in Bash. This downloads four small files and checks each against the commit. Save `BOARD_TOOLS` in the shell for the entire session. Reuse that directory across flashes. Staging transfers the same GBS-built benchmark binary to each image and records its hash. Stage takes seconds to about a minute and uses small native disk space and a small SDB transfer. Identity and process checks take seconds. Microbench runs five iterations and may take several minutes on the TV. Each playback sample takes about one minute. The wrapper retains every command's raw SDB output under the native tools directory and prints at most 240 log lines. Board files and samples are written under `/root/llvm-pm/pm0005-mlgo`.

```bash
BOARD_TOOLS=$(set -euo pipefail; cd /home1/chengkai/vd-tree; d=$(mktemp -d "$PWD/workspace/temp/pm0005-board.XXXXXX"); cd "$d"; export TMPDIR="$d"; printf '%s\n' 'af58f426183177382a060a12400687dbaab0890d08baf3764c7e8cd70ab966cb  mlgo-tv-run.sh.txt' '21070fc762b878343faac9a331235ad2dfde06eb87cfa7f2f5ac24a5b855e5cf  mlgo-tv-identity.sh.txt' '97375b61115fa88c3926b729af117c6f702f1423df7001599145a1861f5c9181  mlgo-tv-measure.sh.txt' '9ece8727da564d33a069b69ccf7187aa43b0f8e803b9c51a6a1e11b5ae776a2e  mlgo-tv-microbench.c.txt' >inputs.sha256; for f in mlgo-tv-run.sh.txt mlgo-tv-identity.sh.txt mlgo-tv-measure.sh.txt mlgo-tv-microbench.c.txt; do curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/2303fa18ff0bc39bd26e8b6dc683bbb24bd7611a/artifacts/scripts/r0005/$f" -o "$f"; done; sha256sum -c inputs.sha256 >&2; printf '%s\n' "$d")
```

```bash
sdb devices | head -30
TV_SERIAL='copy the confirmed device serial from sdb devices'
board() { (set -euo pipefail; cd "${BOARD_TOOLS:?prepare verified board tools}"; sha256sum --status -c inputs.sha256; test -f microbench; test -f microbench.sha256; sha256sum --status -c microbench.sha256; bash mlgo-tv-run.sh.txt "$PWD" "${TV_SERIAL:?set the designated TV serial}" "$@"); }
```

The last recorded SDB endpoint was `192.168.108.13:26101`. The last recorded build stamp was `T-KSU2EJAKUC-0101-PERF-202611171009`. Confirm the device and SDB endpoint before using the tools. The historical capture gives a reference stamp and package count. The full QB-to-board binding still needs the artifact evidence. [Retained board capture](../artifacts/evidence/board-readonly-20261117.txt) If the board requires explicit reconnection, use `sdb connect "$TV_ENDPOINT" 2>&1 | head -30` after setting the confirmed endpoint. Keep the serial and board association fixed even if the IP needs updating.

## Gated board-day checklist

1. **Secure Official and confirm the current control.** Prepare the Official rollback directory from its verified capture. Prepare the tools, record the SDB serial and run `board stage`, then `board identity`. Record the existing picture/power and playback settings used for the test.

   **Pass.** `USB_PREP_READY`, the fixed Official artifact URL, size and archive SHA-256, plus `BOARD_STAGED`, three `BOARD_SHA256` lines and an identity output ending in `BOARD_IDENTITY_END` and `PM0005_REMOTE_EXIT 0`. The recorded build stamp or kernel fingerprint ties this TV to the Official artifact. The previous observation of 2,342 RPMs is a consistency check.

   **If it fails.** Paste the native status or identity output. If the Official bundle is unavailable, keep the current image and obtain the matched replacement pair. If current image identity is inconclusive, stop control measurements until the artifact mapping is established or arrange a separately confirmed Official flash with the tested recovery path.

2. **Capture five Official cold boots individually.** With the TV idle, use the operator-confirmed cold power cycle. For each trial start the same stopwatch at the agreed power-on event and stop when HomeUI is visible and responds to the same directional-key test. Reconnect SDB if needed. Run `board processes` to identify the HomeUI PID, then `board boot official "$N" "$HOME_PID"`, with `N` from 1 to 5. Use the same delay/power procedure and readiness criterion in both lanes.

   **Pass.** Exact HomeUI process confirmed, a distinct `BOOT_ID` and one `BOOT` row for that trial, plus the manual stopwatch value and remote exit 0. `kernel_to_home_process_s` is process start relative to the kernel boot clock. `kernel_uptime_at_collection_s` includes collection delay. The stopwatch provides the separate power-on-to-usable-UI observation.

   **If it fails.** Paste the output and note the last visible screen/SDB status. Same boot ID, ambiguous PID, a warm reboot or a missed stopwatch read invalidates that trial. Get confirmation before replacing it. Stop if HomeUI is unusable or the TV cannot boot.

3. **Run the Official kernel microbench.** Let HomeUI settle, close the player, keep the same peripheral and network state, and agree on an online CPU and comparable starting temperatures. Set `CPU` to that CPU number and run `board micro official "$CPU"`.

   **Pass.** Five `MICRO` rows and remote exit 0. Archive process context, governor if exposed, temperature samples and the benchmark SHA from staging. The columns measure gettid syscall, pipe round trip and first-write minor-fault timing.

   **If it fails.** Paste the output and native log path. Resolve pinning, temperature/load or benchmark progress before retry. Treat thermal or background workload drift as a result qualification issue.

4. **Qualify and play the same 4K stream three times on Official.** No retained evidence identifies a particular 4K clip. The previous USB playback evidence names `mercy/48523_VID_[41][CG]Bolt.ts` and does not establish its resolution. Set `CLIP` to the agreed native path and `USB_CLIP` to the actual mounted USB file. Run the probe and compare the USB file hash to the source. Use a media USB distinct from the flash media.

   ```bash
   (set -euo pipefail; ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,width,height,avg_frame_rate:format=duration -of default=noprint_wrappers=1 "$CLIP"; sha256sum -- "$CLIP" "$USB_CLIP")
   ```

   On TV, open HomeUI → USB → agreed clip → Play/OK. Start from the beginning, wait 10 seconds of uninterrupted playback, then sample 60 seconds with the playback PIDs identified using a pre-trial `board processes` capture. If the core process restarts for each playback, verify the new PID before each sample and keep the sampling window consistent. End playback and return to HomeUI before repeating. Set `N` from 1 to 3 and `MEDIA_PIDS` to the space-separated numeric PIDs in a Bash array. Use `DROPS=NA` until a validated cumulative scalar is available.

   ```bash
   board playback official "$N" 60 "$DROPS" "${MEDIA_PIDS[@]}"
   ```


   **Pass.** Confirm the clip SHA, 3840×2160 or 4096×2160 resolution, duration covering the full sampling window, codec and rate. Each trial has one `PLAYBACK` row with elapsed seconds, system CPU as a fraction of total capacity and selected-process CPU as a percentage of one core. For drop measurement, obtain a documented counter from the active player/video-sink pipeline, confirm the counter tracks only that stream during the window and check that start/end are monotonic without reset. The probe accepts the path of a numeric counter and records both readings. A path/semantics match has not been established on KantSU2E. Report drops as `NA` if unavailable.

   **If it fails.** Paste the `ffprobe` or `PLAYBACK` result and what the TV showed. Stop before reporting a dropped-frame number if its source is unclear. Correct a changed PID, interrupted playback or invalid stream before repeating. Keep CPU results separate from any missing drops.

5. **Preserve control evidence and verify both flash USB directories.** Run `board summary official` and paste it with the Official identity and manual times. Prepare each bundle on the native host. Set `USB_PREP` to that lane's checksummed containing directory, such as `/home1/chengkai/vd-tree/workspace/usb/<QB_ID>`. Set `FLASH_USB` to the confirmed mounted USB root. Copy one lane at a time to a separately labelled drive.

   ```bash
   (set -euo pipefail
    mountpoint -q -- "${FLASH_USB:?confirm the mounted USB root}"
    prep=${USB_PREP:?set the verified QB staging directory}
    (cd "$prep/updateSU2E"; sha256sum --status -c ../manifest.sha256)
    df -h -- "$FLASH_USB"
    target="$FLASH_USB/updateSU2E"
    mkdir -- "$target"
    cp -- "$prep"/updateSU2E/* "$target/"
    sync -f -- "$target"
    (cd "$target"; sha256sum -c "$prep/manifest.sha256")
    printf 'USB_BUNDLE_VERIFIED %s %s\n' "$(basename "$prep")" "$target")
   ```

   Eject each drive cleanly. Keep the Official rollback USB separate and record its label and QB identity.

   **Pass.** Five unique Official boot rows, five microbench rows, three playback rows, independent stopwatch values and frame-counter coverage. All entries in both USB manifests report `: OK` and each command prints `USB_BUNDLE_VERIFIED` with the intended QB ID.

   **If it fails.** Paste the summary or checksum error and keep the TV on Official. Confirm the mounted drive, available space and QB identity. A pre-existing directory requires checking its contents against the intended manifest or selecting a freshly prepared drive.

6. **Enter BOOST with the candidate USB, then pause.** Insert the verified candidate drive while the TV is idle. Reboot the TV and keep pressing the literal `~` on the confirmed input until BOOST appears. At the BOOST prompt enter `mmc`, then stop at the menu. Paste the BOOST/menu text or transcribe the displayed options.

   **Pass.** The expected BOOST prompt and `mmc` option `a` for the full USB image are visible. The confirmed candidate drive has the verified root directory `updateSU2E/`. The Official drive and recovery console are ready.

   **If it fails.** Stop at the prompt or last screen. Paste the menu text/error and confirm the input device and USB detection. Do not select another menu option.

7. **Flash the candidate.** After gate confirmation, select `a` in the `mmc` menu. If a confirmation appears, verify its exact wording and target with the reviewer before accepting. Leave power and USB connected while writing. Wait for the operator-confirmed completion indication and any documented reboot; capture the final console lines.

   **Pass.** The confirmed completion indication, with no reported erase/program/verify error, followed by candidate boot or the agreed next console action.

   **If it fails.** Capture the exact prompt, error and last progress state. While an erase/write may still be active, leave power and USB connected. Once idle and the recovery procedure is confirmed, use Step 10. If the flash state or recovery menu is unclear, stop for board recovery guidance.

8. **Identify and stage the candidate.** Wait for HomeUI and reconnect SDB with the confirmed instructions. Use the existing `BOARD_TOOLS` directory. Run `board stage` and `board identity`.

   **Pass.** The expected candidate identity, including a distinguishing signal tied to the candidate artifact, and the identical measure script and benchmark SHAs from Official. Observe that the planned settings and stable SDB access are present.

   **If it fails.** Paste the console output, identity, device status and any settings differences. Pause on an inconclusive identity, fix a verified SDB access issue if possible, and use Step 10 for a failed boot or unacceptable board state once idle.

9. **Measure and export the candidate.** Repeat Steps 2–4 for lane `custom` with the same CPU, process-selection rule, sample windows, clip SHA, transport and measurement method. Apply the same review gates between trials. Run `board summary custom`; paste it with candidate identity, manual stopwatch values and observations before rollback.

   **Pass.** Five distinct cold boots, five microbench rows, three valid playback samples and an explicit drop-counter coverage status. Note governor/temperature/settings drift and any other environment changes. Record all samples and report medians and spread with those qualifications.

   **If it fails.** Invalidate individual bad samples and retain their error evidence. Use Step 10 for a stability regression or unusable TV after preserving the available evidence. A missing drop counter remains missing data.

10. **Roll back and verify Official.** With the TV idle, remove the candidate flash USB and insert the verified Official rollback USB. Re-check the recorded Official manifest, drive and exact root directory. Reboot and keep pressing `~` until BOOST, enter `mmc`, and paste the menu and selection identity before taking the flash action. After review select `a`, handle the documented confirmation if present and wait for the confirmed completion indication. Reconnect SDB, run `board stage` and `board identity`, and confirm HomeUI plus a short playback smoke.

    **Pass.** The menu gate and flash completion are documented, the running Official fingerprint matches Step 1, HomeUI responds and the known test clip starts.

    **If it fails.** Paste the exact last console state, image/USB identity and SDB output. Leave the device undisturbed during any possible write. If BOOST or completion cannot be confirmed, stop and follow the board owner's recovery procedure rather than attempting another blind flash.

## Open prerequisites for the operator

- Which controller sends `~`, and what exact BOOST/`mmc` prompts, write-completion indication and error-recovery behavior have been seen on this KantSU2E? Does `a` ask for confirmation?
- Which USB partition/filesystem and capacity are proven with this loader? Is the loader case-sensitive, and which image size or extra free-space requirements apply? Use the literal `updateSU2E` in either case.
- Do the full flash and first boot preserve settings, `/root`, network address, SDB authorization and serial-console access? What is the known recovery path if network or HomeUI does not return?
- Which supported power cycle qualifies as a cold boot? Which exact HomeUI process and SDB endpoint should we use?
- Which exact 4K clip and root path should we use, and is there a documented stream-specific dropped-frame counter on this image? Confirm playback process names separately from the counter.
- Which build stamp, running kernel build ID or kernel-file hash ties each newly captured QB to the live board?

## Independent review of MLGO attribution

- **Base swap.** Official 20261113.1 versus Customized 20261118.1 is a kernel-focused Base-swap comparison. The pasted preflight showed 2,952 non-LLVM delta rows. Release bumps still need payload checks. The kernel shelf enables both release advisors in the perf configuration at source level. The actual QB compiler, linker invocation and artifact identity still need corroboration. Exact compiler-package provenance, job identity, kernel config and source, linker, all relevant RPM payloads and measurement conditions determine how precisely a result can be attributed. Hold model-only causal claims until a controlled same-revision A/B changes just the models with otherwise frozen inputs. [Round 0005](../comms/codex_to_claude/0005_reply.md)
- **User-space control.** Compare the actual installed inventories from both images to the two Product/Base resolution chains. The current image comparer covers the retained Official 2,342-RPM roster. Explicitly reconcile candidate-only, removed and unresolved packages, and name every differing ELF even when its package appears in the Base delta. Include workload-relevant non-ELF inputs such as configuration, services, firmware and playback data. Relevant changes inside the expected delta can still affect playback CPU or boot. A matching inventory hash confirms names and versions, while RPM extraction or runtime hashing is needed to assess payload identity. [Current comparison launcher](../comms/codex_to_claude/0005_reply.md#8-candidate-quickbuild-and-image-pair)
- **Kernel replay.** Treat the four-lane TU replay as a diagnosis of advisor activation and code generation. Require the exact verified compiler binaries and actual native/accelerator path. The retained shelf script names `armv7l-tizen-linux-gnueabi-`; the standalone replay's alternate cross prefix needs validation against the derived production compiler/linker and sysroot before attributing results to the QB. Compare identical kernel source, generated headers, flags and normalized paths. Capture default/default as a reproducibility control and show advisor-specific effects when they change an optimization decision. Identical release lanes can reflect the chosen inputs, while default differences require investigation before comparing release results. If production uses LTO, include the relevant production link-time codegen before using the replay to explain emitted kernels. Record missing provenance or unavailable effective QB argv explicitly. [Retained kernel source excerpts](../artifacts/evidence/native-run-r0004-p4-rerun-20261118.txt) [Standalone replay](../artifacts/scripts/r0004/mlgo-kernel-replay.py.txt)

The operator's flat bundle and USB-preparation steps were confirmed for the captured 37654439 layout. Board execution still needs the matched pair, usable rollback, verified GBS-built benchmark and Claude review. The Product comparison found 2,289 differing package files. Record board results as whole-image observations. [Friday report](MLGO_Official_vs_Custom_20261120.md#published-kernel-payload-sizes)
