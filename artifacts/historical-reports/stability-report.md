# VD LLVM Image Stability: Summary Report (up to 2026-10-30)

> Scope: every run-time issue found since the first LLVM image ran on the TV, up to image 20261029.1 (coredumps, libraries that cannot be loaded, functional issues): root cause, fix, verification status, and the next plan.
> The detailed analysis of each issue is in "LLVM Image Stability: Coredump List", version 2 (10-28) and the 10-30 increment.

---

## 1. Conclusion

| Item | Result |
|---|---|
| Images checked | 20261024.3, 20261025.1, 20261027.1 (including the team's re-test of 10-28), 20261029.1; PERF image T-KSU2EJAKUC-0101 |
| Issues found | 14 numbered issues + 1 scan of the whole image (4 libraries that cannot be loaded) + 1 scan of the whole tree for the same code pattern |
| Needed a code or build-file change | 12 packages, all fixed and shelved:<br>· 6 verified on an image as gone (issues 1, 2, 3, 4, 6, 7);<br>· 4 libraries (section 2.2) verified in Quickbuild builds (TEXTREL 0 after rebuild); the re-scan on an image is part of the next image check;<br>· 2 (issues 9, 14) are in the current Quickbuild 37318590, waiting for its image;<br>· 3 more places of the same pattern (pisa-ipc, D.Seal, toybox; section 2.3) were fixed and shelved on 10-30 and go into the image with the next Quickbuild |
| The compiler generated wrong code | **0**. Every issue is a defect that was already in the code or the build scripts and did not show with GCC by chance |
| Not caused by Clang | 5: the ffmpeg timeout, Web Browser, the gst-libav trimming, the contentservicemanager follow-on, and libbroadcastapp-util (the same on the GCC image, fixed as well) |
| Not classified yet | 1: the second crash inside the dotnet signal handler (it hides the first fault; the latest cores are empty); to be re-checked on the new image |
| GCC reference image | No coredumps in the same period; the same library scan finds 0 |

In one sentence: **Clang did not generate wrong code, but it is stricter than GCC and optimises differently, and that exposed a set of hidden defects. Every fix corrects the defect itself and was built with both GCC and Clang; the GCC output is unchanged or changes harmlessly.**

---

## 2. Issues and solutions

### 2.1 Run-time crashes and functional issues

| # | Process / function | Image / count | Symptom | Root cause (one sentence) | Category | Fix (CL) | Status |
|---|---|---|---|---|---|---|---|
| 1 | contentservicemanager, slive-provider-daemon | 10/24, 10/25: 30 | SIGSEGV (assertion) | The framework's `#define INFINITY ~0` is changed to the float infinity by `math.h`, included later; converting it to an integer is undefined behaviour. GCC happened to fold it to `~0`, Clang removed the whole branch | Undefined behaviour | slive-framework: the header restores `INFINITY ~0` after the system headers, plus a static check (14391800) | Verified on image 10/27 |
| 2 | home-mainhub | 10/24, 10/25: 15 | SIGABRT (free of a bad pointer) | Two libraries each have a class `CSourceItemInfo` with the same name and different members; the destructor call was bound by the dynamic linker to the other library's. GCC inlined the destructor, so it never showed | ODR violation | coba-source-native: hidden visibility for its own class (14329307) | Verified on image 10/27 |
| 3 | bt-service | 10/24, 10/25: 5 | SIGBUS | The Clang-only `[[clang::trivial_abi]]` in a header made the Clang-built caller pass the object in a register; the GCC-prebuilt libbluetooth.so reads it by the standard ABI | ABI mismatch (Clang-only attribute + GCC-prebuilt library) | bluetooth-host-impl: `TRIVIAL_ABI` empty in that header (14392070) | Verified on image 10/27 |
| 4 | fw-update-service | 10/24, 10/25: 3 | SIGSEGV (jump to an unmapped address) | At exit, static destruction dlcloses the plug-ins while detached background threads still run in them | Exit ordering | fw-update-service: no dlclose of plug-ins at exit (14392156) | Verified on image 10/27 |
| 5 / 11 | dotnet-hydra-loader (multiscreen; TEMP apps) | 10/25: 1; 10/27: 3; 10/28: 7; 10/29: 2 | SIGSEGV (second crash in the signal handler) | A first segfault in the .NET runtime; the dotnet plug-in's signal handler then uses a null object and crashes again, hiding the first fault; the 2 cores of 10/29 are empty | Open | — | To be re-checked (section 4) |
| 6 | easysetup-daemon | 10/27: 31 | SIGILL (first instruction after exec) | The executable was linked with both `-shared -pie`; GCC's driver lets `-pie` win, Clang's lets `-shared` win, so the output was a shared object without an entry point | Contradicting build flags | `-shared` removed (14391347); the same pattern caught at build time in 3 more TPKs | Verified on 20261029.1 (0) |
| 7 | amd | 10/28: 80 (restart loop after boot) | SIGBUS (alignment) | In aul-1 the server and the client library each have a `Builder` class with the same name and different members; the destructor call was bound to the wrong one. Without amd the whole application framework is down | ODR violation | aul-1: the server-internal classes moved into namespace `aul::server` (14329283) | Verified on 20261029.1 (0) |
| 8 | contentservicemanager | 10/28: 1 | Ended by the watchdog | Application start request timed out while amd was crashing | Follow-on | Gone with issue 7 | Gone |
| 9 | pisa-service | 10/29: 27 (crash loop at boot) | SIGABRT `*** buffer overflow detected ***` | `snprintf(&buf[i*2], sizeof(buf), …)` passes the size of the whole array; Clang computes the space left at -O2, so the FORTIFY check runs; GCC cannot compute it and never checks | Wrong argument (exposed by FORTIFY) | Size changed to `sizeof(buf) - i*2`, the same code in pisa-control-service as well (14398961) | In Quickbuild 37318590, waiting for its image |
| 10 | ffmpeg (TPMS decoding test) | 10/29: 2 | SIGABRT | Ended by the test framework's timeout while decoding normally; not a crash | Not Clang | No action (the performance comparison is tracked separately) | Closed |
| 12 | Web Browser | 10/29 | Exits at start | The browser engine pushed by the store needs an RI API that entered the source on 10-16; the image uses the 10-01 snapshot; the GCC image lacks it too | Not Clang | No action, recorded as a known limitation | Closed |
| 13 | gst-libav (TPMS gstreamer software decoding) | 10/29 | The plug-in registers 1 element | The VD source always defines `TIZEN_PRODUCT_TV`, which deliberately removes 7 register calls; the official GCC image is identical | Not Clang | No action | Closed |
| 14 | libbroadcastapp-util (launchpad preload) | 10/29: log | `dlopen` reports an undefined symbol | The library calls functions of the `-core` library of the same package but is not linked against it; the GCC build is identical | Missing link (not Clang) | The `-core` target added to the link line (14366057) | In Quickbuild 37318590, waiting for its image |

### 2.2 Scan of the whole image: shared libraries that cannot be loaded

Trigger: the team found that libgstomx.so cannot be loaded (`unexpected reloc type 0x03`). All 2236 packages with shared libraries of image 10/27 were then scanned (`TEXTREL` flag, `R_ARM_REL32` dynamic relocations). The same scan of the GCC image: 0.

| Library | Package | Root cause | Fix (CL) | Status |
|---|---|---|---|---|
| libgstomx.so | gst-openmax | The way the spec writes string macros makes libtool's `-fPIC` probe fail with Clang (Clang's warning carries a line number, so the two outputs differ); the whole library was built without position-independent code | The string macros passed on the make command line instead (14396310) | Verified in Quickbuild 37271875 |
| libmmfcamcorder.so | libmm-camcorder | Same | Same (14369000) | Same |
| libSiscMidi.so | gst-ffmpeg | The library's own Makefiles use the executable flags `-fPIE`/`-pie` for a shared library | `-fPIE`/`-pie` removed (14396810) | Same |
| libew-config.so | BM_HWTest | The top-level CMake adds `-fPIE -pie` to the whole tree | `-fPIC` for that library target (14367086) | Same |

### 2.3 Scan of the whole tree for the same pattern (FORTIFY, issue 9)

| Kind | Hits | Would end the process on the LLVM image | Action |
|---|---|---|---|
| `snprintf` family | 44 lines / 24 files | 4 (the same hex-conversion code), all fixed: pisa-service and pisa-control-service (14398961); pisa-ipc (14350530) and D.Seal (14395467) on 10-30 | Size = the space left, names and output unchanged; built with Clang and GCC, shelved |
| `memcpy` / `memset` / `strncpy` etc. | 113 lines / 92 files | 1: toybox `toys/pending/diff.c:800`, `memset(&dir[j], 0, sizeof(dir))`. `dir` is a static array of two elements, so for `j = 1` one element is written past its end, into the next static variable (a real overflow) | Changed to `sizeof(dir[j])` (14409741, 10-30); toybox-full built with FORTIFY runs `diff -r` correctly in the build root |

Conclusion: only a few places are really wrong, and they are fixed one by one in the code. **The FORTIFY check in glibc does not need to be relaxed.**

### 2.4 Root-cause categories

| Category | Count | Packages | Why it did not show with GCC |
|---|---|---|---|
| ODR violation (two different classes with the same name in one process) | 2 | home-mainhub, amd | GCC inlined the destructor, no dynamic binding |
| Undefined behaviour | 1 | slive-framework | GCC's result for float infinity to integer happened to work |
| ABI mismatch (Clang-only attribute + GCC-prebuilt library) | 1 | bt-service | GCC has no such attribute |
| Exit ordering | 1 | fw-update-service | Different timing, hard to reproduce on the GCC image |
| Contradicting link flags `-shared -pie` | 1 (3 more caught early) | easysetup-daemon | The two drivers resolve the contradiction differently |
| Shared library not built as position-independent code | 4 | gst-openmax, libmm-camcorder, gst-ffmpeg, BM_HWTest | libtool's probe passes with GCC; under `-fPIE` GCC still uses the GOT for globals |
| Wrong size argument (FORTIFY) | 1 (3 more of the same fixed in advance: pisa-ipc, D.Seal, toybox) | pisa-service | GCC cannot compute the space left, so no check |
| Missing link in the package | 1 | broadcastapp-util | Same on the GCC image |
| Not a Clang issue | 4 | ffmpeg, Web Browser, gst-libav, contentservicemanager follow-on | — |

---

## 3. How the issues are handled

- **Analysis**: the gdb of Tizen base opens the core in a build environment on the same base as the image; the image's binaries and debug information come from Quickbuild's product repository. For the minimal cores the TV writes, symbols are loaded per file mapping recorded in the core before unwinding. GCC comparisons use the same package from the official GCC image repository.
- **Fix rules**: fix the root cause, no workaround options; every change carries a comment and PLEASE CHECK for the owner; the original execution logic is kept, and no new names or parameters are introduced in other teams' code.
- **Verification**: every fix is built with Clang and with GCC under the Quickbuild conditions (same build.conf, same Base snapshot, same shelve list); whatever can be checked on the binaries (symbols, disassembly, relocations, NEEDED, dlopen) is checked; the final proof is that the issue is gone on the next image.

---

## 4. Next plan

Next week the work runs on two lines:

- **Line 1**: adapt all 891 shelve CLs to the latest VD code and start a new build. The fixes of 10-30 (pisa-ipc, D.Seal, toybox) go into the image with this build.
- **Line 2**: continue with the table below. When the testers are back on Monday 11-02, the image of Quickbuild 37318590 is re-tested first (item 1).

| # | Work item | Content | Done when | Time |
|---|---|---|---|---|
| 1 | Re-test on the image of Quickbuild 37318590 | pisa-service, launchpad preload log; search all logs and coredumps for `*** buffer overflow detected ***`; is dotnet still there | pisa-service and broadcastapp-util: 0 | The day the image is out |
| 2 | Remaining fixes of the same pattern | Done (10-30): pisa-ipc `pisa_ipc_util.cpp:87` and D.Seal `SEALAuthChecker.cpp:237` fixed like issue 9; toybox `diff.c:800` confirmed as a real overflow and fixed. The new toybox CL also restores the platform build flags that the team member's CL had dropped (see the Change Evaluation List, section 4) | Built on both sides, shelved | Done |
| 3 | dotnet second crash | If it still occurs on the new image with a non-empty core: a null check in the signal handler (owner to confirm) that also prints the address of the first fault, then analyse the first fault | First fault located | Depends on the re-test |
| 4 | Fixed checks for every new image | Classify all coredumps; library scan (TEXTREL / REL32); `buffer overflow detected`; launchpad preload failures | One increment per image | Ongoing |
| 5 | ABI risk of prebuilt libraries | For every package marked as prebuilt in the image, check its headers for Clang-only ABI attributes (the pattern of issue 3) | List + conclusion | Next week |
| 6 | ODR risk | Scan the libraries loaded into the same process for exported class-member symbols with the same name (the pattern of issues 2 and 7); the 69 further duplicate symbols of the two home-mainhub libraries go to the owner | List + conclusion | Next week |
| 7 | Run-time check of the TPKs outside the image | The 232 TPKs not in the product image (203 `*-mapi` etc.) installed on the TV by TOMATO and run, compared with the GCC version | No difference | Next week |
| 8 | Compatibility of 3rd-party native apps (HQ question) | ① compare exported symbols and type layouts of the public platform libraries between the GCC and Clang builds; ② audit the public SDK headers (Clang-only attributes, compiler-dependent type definitions); ③ install and run native store apps on the LLVM image | Evidence for whether 3rd parties need to rebuild | After agreement |
| 9 | Owner review | Every PLEASE CHECK change distributed per CL to its owner | Owner confirms or gives the final form | Ongoing |
| 10 | Web Browser | Re-check once the source snapshot is later than 10-16, or the store engine matches the current firmware | The browser starts | When the baseline is updated |
| 11 | Image check after the new build | On the new image of line 1: pisa-ipc, D.Seal and toybox, plus the fixed checks of item 4 | 0 | The day the new image is out |
