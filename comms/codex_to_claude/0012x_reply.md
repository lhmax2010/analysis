# 0012x · November 25 QB capture, pair gate, kernel comparison and USB staging

| Lane | New QB | Product | Expected LLVM Base | Retained reference QB |
| --- | ---: | --- | --- | ---: |
| Official | 37777148 | 20261125.1 | 20261113.1 | 37736448 |
| Custom | 37777264 | 20261125.2 | 20261118.1 | 37736427 |

**One native command, after Claude review.** It can run alongside the existing pm12t jobs using its own pair lock. One low-priority process handles the lanes sequentially. Allow roughly 15–60 minutes, about 3.6 GB of intranet downloads plus kernel RPMs, and about 9–12 GiB additional disk for both captures and expanded USB directories. Keep the 50 GiB reserve and the concurrent job’s own disk allowance. The supplied GBS configs are inputs only. This job performs no GBS build, QB submission or physical USB/device operation.

```bash
(
  set -eu
  cd /home1/chengkai/vd-tree
  p=bf8ecdba7b2911aa0474aae31b8bf018e87f1589
  d=$(mktemp -d "$PWD/workspace/temp/pm0012x-launch.XXXXXX")
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 120 "https://raw.githubusercontent.com/lhmax2010/analysis/$p/artifacts/scripts/r0012x/capture.sh.txt" -o "$d/run"
  printf '%s  %s\n' a01ef28bd59ccfaf6dde6360b59810e1f1d19ba45752acd2b27888295025d82a "$d/run" | sha256sum -c -
  exec bash "$d/run" "$p"
)
```

Return the compact terminal output. Full output, per-package source verdicts and discrepancies are kept at the printed PAIR_WORKDIR. Captures are under workspace/qb-evidence. The job verifies published Product and Base identity, build.conf bytes, submitted-list bytes, active GBS configuration and the entire Product armv7l repository including noarch entries. Release or RPM hash changes with equal source version/VCS are counted separately. Additional XML field differences enter the review packet. A QB number is operator-supplied; each is bound to the requested Product URL and checked against the published Product ID and native GBS config.

The launcher attempts to retain the submitted shelf and Base lists separately for each job from its builddata publication. If submission attachments are invisible, it prints SUBMITTED_INPUT UNPROVED for the missing lane and list. For a rerun, operator-confirmed file paths under vd-tree may be exported as `QB_37777148_SHELVES`, `QB_37777148_BASE_LIST`, `QB_37777264_SHELVES` and `QB_37777264_BASE_LIST`. A mismatch with a published copy fails verification. Historical November 23 lists alone do not bind a November 25 submission. Fully retained captures and completed USB trees are verified and reused on rerun.

| Terminal result | Interpretation |
| --- | --- |
| Two SOURCE_VERIFIED rows | Every included USB file was hashed from the retained PERF tar and matched against the staged file and manifest after the two required name substitutions. Directories are workspace/usb/37777148/updateSU2E and workspace/usb/37777264/updateSU2E. |
| QB_PAIR_PRODUCT_VCS_MATCH and QB_PAIR_GATE PASS | Published sources match on both lanes, submitted lists and build.conf match, and review found only the expected lane endpoints and local GBS root difference. |
| KERNEL_BYTES and KERNEL_BUILD_ID | Prints sizes and SHA-256 for old and new uImage, zImage and perf RPM in each lane. The header and data CRCs, zImage’s uncompressed bytes and unique GNU kernel build ID are checked. The two USB kernel files also match the corresponding SHA-256 entries in their retained RPM. |
| KERNEL_TABLE_BYTES_CARRY_OVER True | Both lanes match all three previous artifacts and the embedded build IDs. Attribute inherited byte/section values to the matched artifact, and keep the original QB labels on board samples. A changed RPM with unchanged kernel bytes requires a new RPM row and investigation of packaged modules/metadata. A changed kernel needs fresh static measurements and boot-resource validation in that lane. |

**Remeasure on the new pair.** Capture board identity, boot route, installed RPM rosters, boot times, idle memory, signed workloads and playback for the new images. Refresh the image-level ELF/Thumb census and user-space comparison, or transfer individual static results only for byte-verified artifacts. Old GBS pilot, kernel-lane and compiler-delivery evidence retain their original source/config/toolchain identity. The November 23 jobs continue against their existing captures. The new gate establishes a Base-swap comparison; narrowing attribution to MLGO alone also requires toolchain and user-space controls.

**Verification so far.** Local Python 3.10 fixtures exercised submitted-list discovery and absence, config substitutions, mismatched source version/VCS, RPM release-only changes, USB renaming, repeated staging verification, GNU build ID extraction and rejection of altered DTB bytes. The actual intranet capture, pair result, old/new kernel verdict and verified USB directories await native output. [Pair fixture](../../artifacts/tests/r0012x/pair.py) · [Kernel relaunch, including the superseding K2/K3 switch](0012y_reply.md)
