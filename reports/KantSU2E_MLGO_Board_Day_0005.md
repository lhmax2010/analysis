# KantSU2E board day for the Official and Customized MLGO comparison

Claude review is pending. Run one numbered step at a time. Paste its compact terminal output and any requested observations. Wait for Claude or Codex to confirm the gate before advancing. Apply that pause to every individual cold boot and playback trial. Record board serial, QB IDs and measurement lane with every batch.

## Independent review of the proposed order

| Proposed step | Correction |
| --- | --- |
| 1. Measure Official first | Establish the currently running image's identity and have a verified rollback image ready before starting. Preserve each result on the native host as it is collected. Five software reboots or five reads of uptime cannot establish five cold boots. |
| 2. Prepare a candidate USB and keep Official available | Verify both flash files and their USB copies before flashing either. A locally calculated digest checks byte consistency. Provenance comes from the fixed QB artifact listing and, when available, its independently published digest. A Product RPM repository may contain no full flash image. |
| 3. Enter BOOST and flash | Separate entering BOOST from selecting `a`. Verify the USB, exact filename, menu text and recovery access first. The key sequence below is the operator's supplied procedure. The completion prompt and error recovery need confirmation on this board. |
| 4. Identify and measure the candidate | Kernel version, package NEVRA and package count are sanity checks and may be shared by both builds. Require a build stamp, running kernel fingerprint or equivalent discriminator tied to the expected image. Reuse the exact benchmark binary and test clip. |
| 5. Roll back immediately on any failure | Recover a failed build or stability regression with a verified Official image when the board is idle and BOOST is available. A bad sample or missing counter only invalidates that result. An uncertain flash state requires recovery guidance before any interruption. Confirm the running Official identity after rollback. |

## Native commands

### Download a flash image

Start only after the running Product comparison exits and releases the heavy lock. Download one image at a time, with Official first for rollback. These are the fixed directory inputs. A directory link establishes the build scope. Verify the exact `updateSU2E` file before preparing a USB.

| Lane | QuickBuild | Product repository | Parent artifacts directory |
|---|---|---|---|
| Official | 37627297 | [Product 20261117.2](http://repos.vd.sec.samsung.net/priv/168.219.236.62:81/PRV/builds/b658/19350658/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2/) | [Artifacts 19350658](http://repos.vd.sec.samsung.net/priv/168.219.236.62:81/PRV/builds/b658/19350658/artifacts/) |
| Customized | 37654439 | [Product 20261118.2](http://repos.vd.sec.samsung.net/priv/168.219.246.226:81/PRV/builds/b993/19368993/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261118.2/) | [Artifacts 19368993](http://repos.vd.sec.samsung.net/priv/168.219.246.226:81/PRV/builds/b993/19368993/artifacts/) |

The four HTTP directory checks and the two HTTPS parent checks timed out from this workspace. The flash-file locations are still unverified. In the intranet QuickBuild UI, open the completed run by its numeric QB ID, open **Artifacts** or the linked image-generation/publish job, and follow the KantSU2e `RELEASE` full-image output. Copy the fixed download link for the exact-case file `updateSU2E`, plus the file length and published SHA-256 if shown. If the UI only lists a bundle, capture its fixed link and the internal path of `updateSU2E`. The current downloader accepts a direct file or browsable directory. Record any board-visible build stamp or kernel fingerprint shown with the artifact.

Set `IMAGE_URL` to the confirmed direct link when available. The downloader can also search one of the fixed directories above. It uses bounded HTML discovery and requires a unique match. For a first pass with directory discovery, use the Product directory. If it has only RPMs and the parent is too broad for a unique lookup, use the exact QB artifact link. Before each lane, unset `QB_SHA256` or set it to the independently obtained digest for that lane. Output stays in `workspace/temp/pm0005-image-*`. Hashing uses modest CPU. A full transfer requires roughly one image's size in disk and network and may take 5–60 minutes or longer.

```bash
(set -euo pipefail; cd /home1/chengkai/vd-tree; d=$(mktemp -d "$PWD/workspace/temp/pm0005-tools.XXXXXX"); export TMPDIR="$d"; f="$d/kantsu2e-image.py.txt"; curl -fsS --connect-timeout 8 --max-time 60 'https://raw.githubusercontent.com/lhmax2010/analysis/2303fa18ff0bc39bd26e8b6dc683bbb24bd7611a/artifacts/scripts/r0005/kantsu2e-image.py.txt' -o "$f"; printf '%s  %s\n' '741c22a2c43e79068ebe91475f033be78c0aef49f53c9b5462edd479fd00cf40' "$f" | sha256sum -c -; args=("${IMAGE_URL:?set the approved fixed image URL}"); if [[ -n "${QB_SHA256:-}" ]]; then args+=(--sha256 "$QB_SHA256"); fi; mkdir -p "$PWD/workspace/temp/pm0005-native-lock"; flock -n "$PWD/workspace/temp/pm0005-native-lock/heavy.lock" python3 -B -u "$f" "${args[@]}")
```

### Prepare and retain the board tools once

The legacy staging command invokes the native cross compiler for the benchmark. Apply the GBS-only build rule before this measurement step. The artifact lookup and downloader above are independent of benchmark staging.

Run on the native server in Bash. This downloads four small files and checks each against the commit. Save `BOARD_TOOLS` in the shell for the entire session. Reuse that directory across flashes. Staging builds the static ARM benchmark once with the approved cross GCC and records its hash. Set `ARM_CC` to the approved cross GCC binary if the default name is missing. Stage takes seconds to about a minute and uses small native disk space and a small SDB transfer. Identity and process checks take seconds. Microbench runs five iterations and may take several minutes on the TV. Each playback sample takes about one minute. The wrapper retains every command's raw SDB output under the native tools directory and prints at most 240 log lines. Board files and samples are written under `/root/llvm-pm/pm0005-mlgo`.

```bash
BOARD_TOOLS=$(set -euo pipefail; cd /home1/chengkai/vd-tree; d=$(mktemp -d "$PWD/workspace/temp/pm0005-board.XXXXXX"); cd "$d"; export TMPDIR="$d"; printf '%s\n' 'af58f426183177382a060a12400687dbaab0890d08baf3764c7e8cd70ab966cb  mlgo-tv-run.sh.txt' '21070fc762b878343faac9a331235ad2dfde06eb87cfa7f2f5ac24a5b855e5cf  mlgo-tv-identity.sh.txt' '97375b61115fa88c3926b729af117c6f702f1423df7001599145a1861f5c9181  mlgo-tv-measure.sh.txt' '9ece8727da564d33a069b69ccf7187aa43b0f8e803b9c51a6a1e11b5ae776a2e  mlgo-tv-microbench.c.txt' >inputs.sha256; for f in mlgo-tv-run.sh.txt mlgo-tv-identity.sh.txt mlgo-tv-measure.sh.txt mlgo-tv-microbench.c.txt; do curl -fsS --connect-timeout 8 --max-time 60 "https://raw.githubusercontent.com/lhmax2010/analysis/2303fa18ff0bc39bd26e8b6dc683bbb24bd7611a/artifacts/scripts/r0005/$f" -o "$f"; done; sha256sum -c inputs.sha256 >&2; printf '%s\n' "$d")
```

```bash
sdb devices | head -30
TV_SERIAL='copy the confirmed device serial from sdb devices'
board() { (set -euo pipefail; cd "${BOARD_TOOLS:?prepare verified board tools}"; sha256sum --status -c inputs.sha256; bash mlgo-tv-run.sh.txt "$PWD" "${TV_SERIAL:?set the designated TV serial}" "$@"); }
```

The last recorded SDB endpoint was `192.168.108.13:26101`. The last recorded build stamp was `T-KSU2EJAKUC-0101-PERF-202611171009`. Confirm the device and SDB endpoint before using the tools. The historical capture gives a reference stamp and package count. The full QB-to-board binding still needs the artifact evidence. [Retained board capture](../artifacts/evidence/board-readonly-20261117.txt) If the board requires explicit reconnection, use `sdb connect "$TV_ENDPOINT" 2>&1 | head -30` after setting the confirmed endpoint. Keep the serial and board association fixed even if the IP needs updating.

## Gated board-day checklist

1. **Secure Official and confirm the current control.** Run [the image downloader](#download-a-flash-image) for Official. Prepare the tools, record the SDB serial and run `board stage`, then `board identity`. Record the existing picture/power and playback settings used for the test.

   **Pass.** `STATUS IMAGE_DOWNLOADED`, the fixed Official artifact URL, size and hash, plus `BOARD_STAGED`, three `BOARD_SHA256` lines and an identity output ending in `BOARD_IDENTITY_END` and `PM0005_REMOTE_EXIT 0`. The recorded build stamp or kernel fingerprint ties this TV to the Official artifact. The previous observation of 2,342 RPMs is a consistency check.

   **If it fails.** Paste the native status or identity output. If the Product URL has no image, open the Official QB web artifact listing and provide the fixed full-image link. If current image identity is inconclusive, stop control measurements until the artifact mapping is established or arrange a separately confirmed Official flash with the tested recovery path.

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

5. **Preserve control evidence and verify both flash USB files.** Run `board summary official`. Paste all completed measurements, Official identity and manual times before preparing to flash. Run the downloader for the verified QB 37654439 full-image link, under the same heavy lock. For each separately labelled flash USB, set `IMAGE_FILE` to the absolute downloaded file, `IMAGE_SHA` to its expected SHA and `FLASH_USB` to that drive's confirmed mounted root. Check the filesystem, capacity and that this is the intended drive. Copy and verify one drive at a time.

   ```bash
   (set -euo pipefail; mountpoint -q -- "$FLASH_USB"; test -f "$IMAGE_FILE"; test ! -e "$FLASH_USB/updateSU2E"; test ! -L "$FLASH_USB/updateSU2E"; df -h -- "$FLASH_USB"; cp -- "$IMAGE_FILE" "$FLASH_USB/updateSU2E"; sync -f -- "$FLASH_USB/updateSU2E"; printf '%s  %s\n' "$IMAGE_SHA" "$FLASH_USB/updateSU2E" | sha256sum -c -; stat -c 'USB_IMAGE_BYTES %s' -- "$FLASH_USB/updateSU2E")
   ```

   Eject each drive cleanly from the mounted host after the check. If a correctly named file is already present, first run the checksum and confirm its identity. A different existing file requires the operator to switch drives or remove the old file deliberately. Keep the Official rollback USB physically separate or verify an alternate copy workflow before advancing. Record the checked artifact-to-drive mapping.

   **Pass.** Five unique Official boot rows, five microbench rows, three playback rows, the independent stopwatch values and the frame-counter coverage displayed. Both USB checks print `updateSU2E: OK` with the expected byte count and both images map to their QB IDs.

   **If it fails.** Paste the summary or checksum error. Keep the TV on Official. Confirm USB filesystem/space, the mount and the QB artifact mapping before retrying.

6. **Enter BOOST with the candidate USB, then pause.** Insert the verified candidate drive while the TV is idle. Reboot the TV and keep pressing the literal `~` on the confirmed input until BOOST appears. At the BOOST prompt enter `mmc`, then stop at the menu. Paste the BOOST/menu text or transcribe the displayed options.

   **Pass.** The expected BOOST prompt and `mmc` option `a` for the full USB image are visible. The confirmed candidate drive has the one verified root file. The Official drive and recovery console are ready.

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

10. **Roll back and verify Official.** With the TV idle, remove the candidate flash USB and insert the verified Official rollback USB. Re-check the recorded Official SHA, drive and exact root filename. Reboot and keep pressing `~` until BOOST, enter `mmc`, and paste the menu and selection identity before taking the flash action. After review select `a`, handle the documented confirmation if present and wait for the confirmed completion indication. Reconnect SDB, run `board stage` and `board identity`, and confirm HomeUI plus a short playback smoke.

    **Pass.** The menu gate and flash completion are documented, the running Official fingerprint matches Step 1, HomeUI responds and the known test clip starts.

    **If it fails.** Paste the exact last console state, image/USB identity and SDB output. Leave the device undisturbed during any possible write. If BOOST or completion cannot be confirmed, stop and follow the board owner's recovery procedure rather than attempting another blind flash.

## Open prerequisites for the operator

- Which controller sends `~`, and what exact BOOST/`mmc` prompts, write-completion indication and error-recovery behavior have been seen on this KantSU2E? Does `a` ask for confirmation?
- Which USB partition/filesystem and capacity are proven with this loader? Is the loader case-sensitive, and which image size or extra free-space requirements apply? Use the literal `updateSU2E` in either case.
- Do the full flash and first boot preserve settings, `/root`, network address, SDB authorization and serial-console access? What is the known recovery path if network or HomeUI does not return?
- Which supported power cycle qualifies as a cold boot? Which exact HomeUI process and SDB endpoint should we use?
- Which exact 4K clip and root path should we use, and is there a documented stream-specific dropped-frame counter on this image? Confirm playback process names separately from the counter.
- Can the QB web artifacts provide the exact Official and candidate full-image links and published digests, plus an image-specific build stamp, kernel build ID or kernel-file hash to map to the live board?

## Independent review of MLGO attribution

- **Base swap.** Official 20261113.1 versus Customized 20261118.1 is a kernel-focused Base-swap comparison. The pasted preflight showed 2,952 non-LLVM delta rows. Release bumps still need payload checks. The kernel shelf enables both release advisors in the perf configuration at source level. The actual QB compiler, linker invocation and artifact identity still need corroboration. Exact compiler-package provenance, job identity, kernel config and source, linker, all relevant RPM payloads and measurement conditions determine how precisely a result can be attributed. Hold model-only causal claims until a controlled same-revision A/B changes just the models with otherwise frozen inputs. [Round 0005](../comms/codex_to_claude/0005_reply.md)
- **User-space control.** Compare the actual installed inventories from both images to the two Product/Base resolution chains. The current image comparer covers the retained Official 2,342-RPM roster. Explicitly reconcile candidate-only, removed and unresolved packages, and name every differing ELF even when its package appears in the Base delta. Include workload-relevant non-ELF inputs such as configuration, services, firmware and playback data. Relevant changes inside the expected delta can still affect playback CPU or boot. A matching inventory hash confirms names and versions, while RPM extraction or runtime hashing is needed to assess payload identity. [Current comparison launcher](../comms/codex_to_claude/0005_reply.md#8-candidate-quickbuild-and-image-pair)
- **Kernel replay.** Treat the four-lane TU replay as a diagnosis of advisor activation and code generation. Require the exact verified compiler binaries and actual native/accelerator path. The retained shelf script names `armv7l-tizen-linux-gnueabi-`; the standalone replay's alternate cross prefix needs validation against the derived production compiler/linker and sysroot before attributing results to the QB. Compare identical kernel source, generated headers, flags and normalized paths. Capture default/default as a reproducibility control and show advisor-specific effects when they change an optimization decision. Identical release lanes can reflect the chosen inputs, while default differences require investigation before comparing release results. If production uses LTO, include the relevant production link-time codegen before using the replay to explain emitted kernels. Record missing provenance or unavailable effective QB argv explicitly. [Retained kernel source excerpts](../artifacts/evidence/native-run-r0004-p4-rerun-20261118.txt) [Standalone replay](../artifacts/scripts/r0004/mlgo-kernel-replay.py.txt)

Both QB IDs and their Product directories are now known. The internal directories timed out here. The two exact full-image URLs, sizes and digests await native or QuickBuild artifact evidence. The image helper passed local Python 3.10.12 fixtures. Board scripts passed syntax checks and the microbenchmark compiled locally. KantSU2E execution still awaits the reviewed sequence.
