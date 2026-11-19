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
