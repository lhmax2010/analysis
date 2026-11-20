# Official image ARM-predominant provenance, 19 November

The cohort has 609 loadable ELF files from the completed 2,342-RPM scan. A producer marker can come from one object linked into a file. Multiple strings in an ELF do not identify which one emitted its A32 instructions. [Completed scan](../evidence/native-run-r0005-argot-scan-gbs-20261118.txt#L185)

| ELF producer markers | External producer, verified | Bundled prebuilt, same-NEVRA spec evidence | Rebuilt in QB, verified per file | Origin unverified | Total |
|---|---:|---:|---:|---:|---:|
| GCC | 0 | 4 | 0 | 153 | 157 |
| GCC + Clang | 0 | 0 | 0 | 445 | 445 |
| GCC + Rust | 2 | 0 | 0 | 2 | 4 |
| None | 0 | 0 | 0 | 3 | 3 |
| Total | 2 | 4 | 0 | 603 | 609 |

The two argot files have evidence that the package copies artifacts from the external cargo-tizen build. The four `vd_memps` files have exact packaged paths and a retained `0.3.5-1` spec that installs the prebuilt bpftrace binary and copies its bundled libraries. The retained top-40 rows match the paths for `bpftrace32` and the three LLVM/Clang 19 shared objects. This is packaging-origin evidence for those files. The original cause inventory remains **2 PREBUILT / 607 UNRESOLVED**. The native provenance view tracks the four additional candidates in their own packaging-evidence column and leaves the original per-ELF ISA cause intact. [Argot producer readback](../evidence/native-run-r0005-pic-accel-argot-20261118.txt#L70) [Packaging source excerpt](../evidence/vd_memps-bpftrace-spec-excerpt-20261119.txt) [Cause run](../evidence/native-run-r0006-causes-kernel-sections-20261119.txt#L82)

For `qte-bm`, Widevine, PlayReady, preload containers and the Python 3.5 binary, the paths and marker strings identify targets for spec/RPM inspection. A TPK layer or `/opt/usr/apps` location does not establish a prebuilt producer. The native table splits unverified paths into nested archive members, direct app paths and other direct paths, attaching the Official source RPM identity, route and binary RPM SHA where available. A source RPM field alone proves neither that an ELF was compiled in QuickBuild nor that it was copied. A verified rebuild classification requires a source/install trace, exact historical build log or output-to-payload match. [Native launchers](../../comms/codex_to_claude/0006_reply.md#thumb-provenance-and-compile-commands)

The Official platform macro sets `CC=armv7l-tizen-linux-gnueabi-clang`, corresponding `CXX=...clang++`, and `AR=llvm-ar`. The resulting C/C++ flags include `-mthumb`; the macro expands `-flto -ffat-lto-objects` into CFLAGS, CXXFLAGS and FFLAGS in this probe. A build that passes the mode flag through on its C compile command requests Thumb unless another setting supersedes it. Investigate dropped flags, explicit `-marm`, per-function `target("arm")`, assembly mode directives and packaged prebuilts. Check final argv, including flag order and response files, then map each object to the packaged ELF. [RPM build trace](../evidence/native-run-r0006-thumb-fail-kernel-isa-20261119.txt#L11)

`glibc` contributes 22 files and `glibc-locale` 45. Their pinned Base source RPM is `glibc-2.40-1.111.src.rpm`. The retained packaging diff applies the GCC override because glibc uses GCC extensions. The build source of the mode choice and any ARM assembly remain unverified. Check the Official OBS build log, matching source spec and per-object assembly/C commands before assigning `GLIBC_MARM`. [Retained OBS packaging diff](../evidence/glibc-obs-toolchain-override-20261119.diff.txt) [RPM payload inventory](rpm-payload-plan-part-04.csv) [Native cause counts](../evidence/native-run-r0006-causes-kernel-sections-20261119.txt#L213)

## Round 0007 force-options readback

| Marker | Proven external producer | Bundled via spec | Unverified archive member | Unverified direct app | Unverified direct | Files | Estimated A32 bytes |
|---|---:|---:|---:|---:|---:|---:|---:|
| GCC | 0 | 4 | 45 | 12 | 96 | 157 | 195,428,887 |
| GCC + Clang | 0 | 0 | 28 | 26 | 391 | 445 | 141,199,741 |
| GCC + Rust | 2 | 0 | 0 | 0 | 2 | 4 | 12,982,977 |
| None | 0 | 0 | 1 | 2 | 0 | 3 | 10,134,602 |
| Total | 2 | 4 | 74 | 40 | 489 | 609 | 359,746,207 |

The GCC C probe used the generated `/usr/bin/gcc` wrapper, byte-identical to the prefixed GCC wrapper. The regular branch calls the resolved `-real` program with the original argv followed by `-mthumb -O2` and the other policy options, including `-fstack-protector-strong -Wshadow -Werror`. The ordering in the file governs ordinary invocations without an upstream bypass or per-function ISA controls. The same shell logic sends the escape option to collect2 for invocations whose arguments match `__KERNEL__` or `-nostdlib`, and has a separate UBSan/PCH branch. The `$t` from plain `gcc -c` therefore establishes the wrapper path result. The effective C++ argument list and production activation are pending. [Wrapper evidence](../evidence/native-run-r0007-gcc-force-wrapper-20261120.txt)

The tested unflagged Clang driver emits `$a` with and without its three-line config. The platform-flag invocation emits `$t`. An input that drops the ISA flag is a plausible source of A32, as are a later `-marm`, individual source mode controls and uninstrumented or prebuilt code. The 445 mixed-marker ELFs are a screening population. Some large suspected blobs (the Qt bundle, DRM and Python examples) are in this mixed-marker population. The 157 GCC-only entries include 153 with unresolved origin. Prioritize glibc/glibc-locale (67 paths), then classify object-level usage with source and final argv, separating wrapper exemptions, direct compiler bypass, assembly and prebuilts. Link-only `-nostdlib` says nothing about the ISA of a preceding compile. [Driver trace](../evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L542) [Origin readback](../evidence/native-run-r0006-fullscan-thumbprobe-20261119.txt#L434)

The previous per-file ISA cause inventory remains 2 PREBUILT and 607 UNRESOLVED. A32 byte estimates in this table are inventory weights, with no measured savings attached. The 609 entries are loadable user-space ELFs. The 180 REL module paths reported by the membership view are separate. [Methods and planned samples](../../comms/codex_to_claude/0007_reply.md)


## Round 0008a Product policy confirmation

Both Product build.conf files include `Preinstall: gcc-warning-build-env` and `RunScripts: gcc-warning-build-env`. The Product-configured GBS log shows preinstall and postinstall of `gcc-warning-build-env-14.2.0-4.1.armv7l` from the Official Base. The C++ wrapper adds `-Wdeprecated-copy` in place of the four C-only warnings. The shared option tail includes `-mthumb -O2 -fstack-protector-strong`. Package and invocation exemptions remain relevant. Both Base OBS build.conf digests match and omit the Product force-options setup. Glibc's Base build needs independent evidence for its effective ISA. [Product and Base configs](../evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L85) [Wrapper and hooks](../evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt#L119)

The retained 10.0 Base clang-contrib source uses RPM build hooks to put options into `clang.cfg` and `clang++.cfg` and remove them after the build. Explicit command-line flags retain precedence. The native readback checks both exact published `clang-force-options-1.0.0-1.1` RPMs. This mechanism is a possible carrier for the scoped config-default experiment. A tail-appended argument policy requires another driver mechanism. [Round 0008a](../../comms/codex_to_claude/0008_reply.md#round-0008a-native-results)
