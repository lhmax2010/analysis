# Round 0012e • Thumb-2 adaptation and acceptance

**Three package fixes and the scoped default are ready for review. No package has passed native T1–T8 in this round.** The test baseline is LLVM Official QB 37736448, Product 20261123.2, Base 20261113.1, published build.conf@14452507. The historical 609 counts ARM-predominant files in a different capture. This inventory includes every mapped A32 span in .text, including mixed ELFs. The full Official roster, group shares and measured deltas require the native image and build roots.

## Tuesday pilot

| Package or control | Evidence in hand | Package lane |
|---|---|---|
| org.tizen.AVControl | The retained spec replaces CXXFLAGS with its EFL define. | Append the define to inherited flags. |
| org.tizen.tv-viewer | The retained spec replaces CFLAGS with its EFL define. Later commands prepend linker options. | Preserve CFLAGS at the first assignment. Check the effective flags for C++ separately. |
| libpisa-ipc | Lines 95–96 replace CFLAGS and CXXFLAGS with a fixed list. | Preserve inherited flags and append the package list, retaining its explicit -O2, hardening and defines. |
| org.tizen.webserver | Retained spec lines 174–178 already preserve CFLAGS and CXXFLAGS. | Inspect the consuming CMake target, source line and actual argv. |
| nnstreamer | Retained spec lines 989–999 transform inherited flags. The visible edits target C++ standard, optimization and coverage. | Identify the failing Meson/Ninja target or prebuilt input from its compile evidence. |
| libgcrypt, rpm | The affected installed file and its native source/argv need a matched join. | Retain baseline/default runs, inventory assembler and collect make check evidence. |
| bluetooth-impl-sec-oal, widevine-cdm | Two explicit -marm controls. | Identical source in all three lanes. Compare mapping and bytes. |

Every pilot gets fresh baseline and default roots. The three source fixes and both controls also get the package lane. For the remaining four, the runner records `PENDING_MATCHED_SOURCE_FIX` and keeps their acceptance open. Each package lane is independent of the scoped default. A package fix can restore -Os and other inherited flags as well as -mthumb. A measured delta from that lane must carry that qualification.

The exact default diff is for `/usr/bin/clang.cfg`. The build-root helper package is `clang-force-options` from clang-contrib. It writes the marked config block and clang++ uses the corresponding config. The local armv7l build.conf enables that helper for eligible packages, and exempts kernel and external-module producers. Keep explicit driver -marm and assembler .arm precedence. The driver probe covers four C/C++ driver names and an explicit -marm case. The full per-build config diff is retained in each lane. No production submission has been made. [Patch set and checksums](../../artifacts/patches/thumb2/SHA256SUMS) · [Scoped default](../../artifacts/patches/thumb2/scoped-clang.cfg.diff)

## Image and source attribution

The image job walks the actual Official partitions and nested supported TPK/ZIP members. It joins an installed path to its RPM database owner and source RPM. Separate debuginfo needs a matching build ID and .text address and size. The returned JSON carries mapped ranges, functions overlapping ranges, endpoint DWARF locations where available, unidentified .text and read errors. Endpoints help locate the compilation unit. They do not prove flag loss. Use the actual compile argv with the enclosing source rule for group (a), source/assembly directives for (b), the explicit flag and documented requirement for (c), packaging provenance for (d), and kernel/module ownership for (e). Raw kernel images outside the ELF inventory are tracked by the separate kernel trial.

The group denominator is measured A32 bytes, with an explicit unresolved class and an independent unmapped .text total. An earlier marker-only estimate cannot fill in those bytes. For a file with mixed causes assign disjoint byte ranges. Qualification checks Official SHA, source owner, non-overlap and exact mapping limits. The checked-in cause ledger currently contains its schema. **After the image readback, review the range evidence, commit the populated ledger and new patches, and re-pin the manifest before launching the full roster.** Running the original pin a second time would use the same empty cause ledger. [Cause ledger](../../artifacts/ledger/official-37736448-thumb-reviewed.tsv) · [Roster](../../artifacts/scripts/r0012e/thumb-roster.py.txt) · [Qualification](../../artifacts/scripts/r0012e/thumb-qualify.py.txt)

## Native schedule and readback

Use the SHA-checked `pm12` launcher function and `pm12read` in the companion reply, on the native server after Claude's review. Current scripts are pinned to `0a4e9ec3592aa1fa870d7b2aa0119426a1f40220`. This server cannot be reached from the local review checkout. [Copyable launcher and resource estimates](0012c_reply.md#native-command-order-for-claude-review)

| Slot | Command after defining the launcher | Returned evidence |
|---|---|---|
| Tuesday night, Wed-A | `pm12 wed-a` | Seven package and two control logs, three lane results when a reviewed hunk exists, per-package acceptance JSON. |
| Wednesday, image slot | `pm12 image` | Same-image installed header checks, full roster and classified/unknown byte denominators. Return the compact combined file and roster packet for review. |
| Wednesday night, after the populated ledger and its updated pin | `pm12 wed-night "$PM12_IMAGE_RUN"` | Full reviewed group (a) and both controls, then scheduled Step 8 lanes with the remaining budget. |
| Thursday, after reviewing failures | `PM12_IMAGE_RUN="$PM12_IMAGE_RUN" PM12_RETRY_PACKAGES="$FAILED_PACKAGES" pm12 thu "$PM12_WEDA_RUN" /home1/chengkai/vd-tree/workspace/temp/pm0011f-batch.xkHDpd` | Kernel trial if the effective config and pinned source are established, repaired packages, existing T7/ABI jobs. Set FAILED_PACKAGES to a space-separated reviewed list, or empty for no package retries. |

PM12_IMAGE_RUN and PM12_WEDA_RUN are the explicit directories printed for those jobs. Each batch has status.txt, combined.txt and separate full logs. Each lane uses its own GBS-ROOT and local repository. The kernel module sub-builds populate their initially empty repository with that lane's kernel-devel RPM. Native traffic is source/dependency reads plus pinned script downloads. Up to six build cores, one heavy job, with 24 GiB disk/12 GiB RAM gates for package lanes and 55 GiB/16 GiB for the kernel. Total storage depends on the retained roots. Several hours to overnight per batch is a planning allowance. A blocked package is recorded and other jobs proceed. Access to the two board lanes and a new QB are outside this run.

For a failed package, take its exact `run` and `package` from status.txt. Return the observed cause, lane, compiler/linker line, log path and relevant acceptance gates. The compact commands below work on the native server.

```bash
pm12read "$run"
job="$run/jobs/thumb-$package"
if [ -f "$job/thumb-acceptance.json" ]; then
  python3 -B "$run/development.py.txt" packet "$job/thumb-acceptance.json" 1
else
  tail -n 25 "$job/job.log"
fi
```

## Friday acceptance and board handoff

| Gate | Evidence retained | What leaves the row open |
|---|---|---|
| T1 Delivery | DWARF producers joined with executed cc1 triples/compilation units, effective mode and response-file coverage | Unread responses, ambiguous or missing CUs, a lost -mthumb or unverified compiler path |
| T2 ISA | Per-installed-path mapping ranges, mapped A32 functions and remaining bytes | Unknown bytes or an A32 residue without an approved source/function explanation. Mixed intentional residue needs review. |
| T3 Size | Same owned path set, .text and SHF_ALLOC, compressed RPM, cpio bytes and installed size | Missing or changed path/RPM scope |
| T4 ABI | SONAME, ordered DT_NEEDED, symbol version definitions and abidiff with matched debuginfo | Dependency/definition differences, missing or ambiguous debug provider, abidiff failure |
| T5 Tests | Spec %check, actual make check for rpm and libgcrypt | No-test status needs source inventory. A marker at the end of an empty test section is insufficient. |
| T6 Smoke | GBS-root A32→Thumb→A32 call, changed DSO dlopen(RTLD_NOW) and symbol/version resolution, approved executable no-op | Daemon/UI executable with no validated start/stop fixture or insufficient runtime dependencies. The first fixed no-op is /usr/bin/rpm --version. |
| T7 Assembly | Source file/line inventory including inline asm and .S, compile evidence, ISA map | Sites still awaiting source-to-function proof, generated code, or assembly edits without review |
| T8 Controls | Both explicit -marm package runs, unchanged payload ELF bytes and mapping, assembled .arm symbol | A single differing control stays in review. |

Kernel trial uses the pinned 14293732 + 14427407 source and requires evidence for the effective Official perf config. It performs baseline and CONFIG_THUMB2_KERNEL=y builds, captures Linux image sizes and linked .text, then builds installed out-of-tree module producers against each lane's kernel-devel. It checks local header identity inside the GBS root and retains expected/produced .ko paths, compile evidence and two statuses per producer. Only a successful matched baseline followed by a failed Thumb build with correct headers supports a Thumb regression. Dependency failures, an unavailable owner/VCS, or a header mismatch remain separate. The linked Linux ELF is required for the kernel .text result. /seret and the detached BTF file have different uses.

**Data available for Doc 07 / Doc 04 today:** three source fixes validated on the retained specs, seven pilot packages and two controls, zero native acceptance results returned in this round. Leave the new Official group-byte shares, package-size deltas and pass counts blank. [Local validation](../../artifacts/evidence/local-r0012c-validation-20261124.txt)

When KantSU2E returns, freeze the exact ELF hashes and paths from the accepted lanes. For tv-viewer measure cold startup to first picture, channel change and sustained 4K playback; include tv-viewer and tvcontrol-notify-manager PSS/USS. For AVControl exercise play/pause/seek and AV sync; for libpisa-ipc measure round-trip request latency through its production caller. For webserver exercise a fixed local request set; for nnstreamer use a fixed pipeline/input and compare output and throughput. Exercise the same fixed crypto workload through libgcrypt, and query the same installed RPM set with /usr/bin/rpm. Verify both explicit controls through Bluetooth and protected playback. Alternate baseline and candidate on one board, retain build and ELF hashes, five repetitions for start/latency/memory and three for 4K CPU/drops. Use identical media, settings and counter source. Define service-specific regression tolerance and soak duration with owners before the run. Static/code-size deltas alone cannot establish PSS or frame-drop changes.
