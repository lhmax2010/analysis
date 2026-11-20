# Clang Migration: Data Requested by HQ (12 Nov 2026, updated 12 Nov evening)

The four lists requested by HQ are given below:

1. packages built with a hard-coded gcc / g++, with before / after;
2. packages not using the global optimisation level;
3. packages without LTO, and the effect of LTO in the LLVM build;
4. other compilers and toolchains (musl-gcc etc.).

## 0. Data sources and method

| | GCC image | LLVM image |
|---|---|---|
| Base | `tizen-10.0-base-standard_20260916.1` | `tizen-10.0-base-dev-llvm-standard_20261105.1` |
| Product | `TIZEN-ONEMAIN-KantSU2e-RELEASE_20261001.3` (new GCC baseline) | `TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261112.1` (Quickbuild of 11 Nov) |
| Global flags | `-O2`, GCC LTO | `-Os`, LLVM LTO (`-flto -ffat-lto-objects`) |

- **Scope.** Only the armv7l repositories were scanned. Host-side and cross packages (x86_64 / aarch64 / riscv64) are not counted.
- **How each file was classified.** Every binary package was downloaded from the official repositories, excluding debuginfo, docs and locale packages. Every ELF file in it was read directly:
  - the `.comment` section shows which compiler built the file;
  - the `.symtab` FILE symbols show whether the file was linked with LTO;
  - section sizes were taken from the section headers.
- **Build logs.** The build logs of the two Base snapshots were parsed for the `-O` level of every compile command. The product repositories do not publish build logs, so for product packages the spec files were scanned instead.
- **Base dates.** The two Base snapshots are not from the same date, so a few packages differ in version.

Totals (armv7l repositories):

| | GCC image | LLVM image |
|---|---|---|
| ELF files | 13,169 | 13,350 |
| Built by clang | 80 | 9,967 |
| ARM ELF built by GCC only | 8,679 | 903 |
| Rust / Go | 163 / 20 | 163 / 20 |
| musl | 0 | 0 |
| ELF linked with LTO (yes / no / unknown: no symbol table) | 5,688 / 5,723 / 1,758 | 5,621 / 5,976 / 1,753 |

## 1. Packages built with a hard-coded gcc / g++

### 1.1 Fixed: the build now follows the toolchain of the build environment

In all of these packages the Makefile, CMakeLists or spec named gcc / g++ itself (`CC = gcc`, `CMAKE_C_COMPILER gcc`, `toolset=gcc`, FFmpeg configure without `--cc`, ...). So the package was silently built by GCC even in the Clang build: without LTO, without the Clang flags, and at its own `-O`.

**How it was fixed.** The fix passes the compiler of the build environment (`CC` / `CXX`). A GCC build still gets gcc / g++, so it is unchanged. Real code defects that showed up once the package was built by clang were fixed in the code.

**What "before" and "after" mean in the table.**
- "Before" is the GCC image.
- "After" is the LLVM image 20261112.1, for the packages whose CL was already in that build. The other CLs go into the next Quickbuild.

| Package | CL | GCC image: ELF / .text KB | LLVM image: clang ELF / GCC-only ELF / .text KB | .text | Status |
|---|---|---|---|---|---|
| boot-sound | 14448478 | 2 / 217 | 2 / 0 / 171 | -21.5% | in the image |
| libtv-player | 14448588 | 3 / 1284 | 3 / 0 / 1157 | -9.9% | in the image |
| ppi-display-control | 14448500 | 2 / 43 | 2 / 0 / 49 | +15.9% | in the image |
| libav-common | 14450650 | 3 / 5586 | 0 / 3 / 5586 | - | next Quickbuild |
| gst-plugins-httpdemux | 14451112 | 5 / 764 | 2 / 3 / 757 | - | next Quickbuild |
| SZDrv_tools | 14448692 | 2 / 370 | 0 / 2 / 370 | - | next Quickbuild |
| streaming-accelerator | 14448705 | 3 / 525 | 1 / 2 / 525 | - | next Quickbuild |
| mdnsresponder | 14450591 | 3 / 198 | 1 / 2 / 175 | - | next Quickbuild |
| feature-config-daemon | 14448709 | 3 / 182 | 2 / 1 / 183 | - | next Quickbuild |
| nvt-pba-interface | 14448696 | 1 / 77 | 0 / 1 / 77 | - | next Quickbuild |
| vdlinux-usb-modules | 14448698 | 2 / 1 | 0 / 2 / 1 | - | next Quickbuild |
| luabind | 14452018 | 2 / 328 | 1 / 1 / 291 | - | next Quickbuild |
| soc-ir-interface | 14452133 | 2 / 26 | 0 / 2 / 26 | - | next Quickbuild |
| lib-ndp-pq-interface-tv | 14452243 | 1 / 79 | 0 / 1 / 79 | - | next Quickbuild |
| soc_vendor-user-bins | 14452503 | 7 / 147 | 0 / 7 / 147 | - | next Quickbuild |
| gst-plugins-dash | 14452597 | 9 / 3737 | 8 / 1 / 3439 | - | next Quickbuild |
| iotivity | 14452627 | 20 / 2133 | 0 / 20 / 1857 | - | next Quickbuild |
| request-support, remote-management, smarthub-connection-test, display-control-impl-sec, UsbSyncDisplay, capi-mva-contextfw, capi-stt-wrapper-tv, capi-va-policy-tv, capi-voice-source-manager-tv | 14448576, 14448314, 14448485, 14448571, 14448681, 14448652, 14448672, 14448655, 14448674 | | | | next Quickbuild |

Code defects found while moving these packages to clang (fixed in the same CLs):
- `log_print()` calls with arguments that their format string does not use (soc-ir-interface);
- `sdp_dpreg_write_array()` collected the register access results but always returned 0, so failures were not reported (lib-ndp-pq-interface-tv);
- an implicit conversion between two enum types (lib-ndp-pq-interface-tv);
- `sscanf("%20[^-]...%20s")` into `char[20]` buffers, a one-byte overflow with a long argument (soc_vendor-user-bins);
- linker options (`-Wl,-z,relro` etc.) placed in CFLAGS of a compile-only rule, so they never reached the linker, in the GCC build either (soc_vendor-user-bins);
- in the DRM decryption path of the Matroska demuxer: a pointer read before it is set, a `memcpy` of 16 bytes past the packet data, a buffer allocation check on the wrong packet, and an uninitialised crypt/skip pattern value (gst-plugins-dash);
- ad-event flags tested with `&&` instead of `&`, so any set flag overwrote the event time and duration (gst-plugins-dash);
- a 64-bit timestamp difference passed to `abs()` / `labs()`, which are 32-bit on armv7: the 8-second audio/video gap check could never trigger (gst-plugins-dash);
- a bitrate-switching parameter declared `int` and initialised with 1.5, so it was 1 (gst-plugins-dash);
- clang identified as GCC 4.2 by a version check, so a different atomic implementation was selected than in the GCC build; a thread function with the wrong signature for `pthread_create` (iotivity).

These fixes change runtime behaviour where the old code was wrong; each place is marked for the owner's review.

**In progress** (verified locally under the Quickbuild conditions, not yet passing):
- org.tizen.webserver: the compiler setting is fixed (`platforms/Tizen.mk` forced gcc / g++); the bundled fcgi library does not yet build with clang;
- gst-plugins-atsc3: built through `cosmos.sh`, which the local gbs setup cannot run yet.

### 1.2 ELF still built by GCC in the LLVM image (903 ARM ELF in 86 packages)

| Group | Packages (GCC-only ELF in the LLVM image) | Status |
|---|---|---|
| Toolchain, GCC by design | glibc (44), gcc (41), gcc-aarch64 / -armv7hl / -riscv64 (22 each), binutils (35), vdprelink (2) | stays GCC |
| GCC forced in the spec (`_toolchain_override`) | yaca (21) | to be reviewed |
| Cross / development tools, not installed on the TV | binutils-aarch64 / -armv7hl / -riscv64 (29 / 29 / 26), gdb (3), sdk-core (8), rust (1) | stays as is |
| Prebuilt or vendor binaries (all ELF GCC, no source build seen) | lib-opengl-es-g52-tv (5), chromium-efl (19), com.samsung.tv.cobalt (12), trustzone-tee-base (28), wifi-drivers-RTK / -MTK (3 / 12), performeter (2), theme-resource, contentimageapp, uem-client, camera firmware updaters, onboot-nvt (9), ppp (2), usb-modeswitch (2) | to be checked package by package (prebuilt binaries cannot change) |
| Part of the package still GCC | hal-rootstrap (286), iotivity (20), gst-plugins-atsc3 (19), org.tizen.tts-engine-neural (19), trustzone-tee (19), bluetooth-impl-sec (16), soc_vendor-user-bins (7), vd_memps (7), org.tizen.UsbSyncDisplay (9), wifi-drivers-MTK (12), easysetup-daemon (3), webserver (3), rdm-client (3), gst-plugins-ss (3), vdtools (3), atsc3uhdcp (3), tztv-kernel (5), native-home (4) and about 30 packages with 1-2 ELF | the top ones are in progress (1.1); the rest are next |

## 2. Packages not using the global optimisation level

The nominal GCC lane uses `-O2` and `-fstack-protector-strong`, while the sampled LLVM optflags use `-Os` and `-fstack-protector`. Package options can win in exempt or unwrapped builds. For affected GCC builds, the force-options wrapper appends `-O2`, `-fstack-protector-strong` and `-mthumb` after the package options. Confirm the effective options per package before interpreting a GCC/Clang size or performance comparison. [Historical wrapper and exemption analysis](optimization-analysis-part-01.md#L285) [Retained GBS wrapper](../evidence/native-run-r0007-gcc-force-wrapper-20261120.txt)

### 2.1 Base packages (from the armv7l build logs: `-O` of every compile command)

| Package | GCC image | LLVM image | Note |
|---|---|---|---|
| glibc | -O2 15539, none 1048 | -O2 15539, none 1048 | GCC by design |
| gcc, gcc-aarch64 / -armv7hl / -riscv64 | -O2 | -O2 | toolchain |
| binutils (and cross variants) | -O2 | -O2 | toolchain |
| gdb | -O2 | -O2 | tool |
| vdprelink | -O2 | -O2 | tool |
| cmake | -O3 845, -O2 305 | -O3 845, -Os 305 | own -O3 |
| ccache, doxygen, jsoncpp, libjpeg-turbo, libwebp, unzip, zip, zstd | -O3 | -O3 | own -O3 |
| libsolv | -O3 157, -O2 1 | -O3 157, -Os 1 | own -O3 |
| perl | -O2 326 | -Os 163, -O2 163 | half of the files own -O2 |
| tcl | -O2 216 | -Os 174, -O2 42 | partly own -O2 |
| strace | -O2 280 | -Os 279, -O2 1 | follows global |
| libgcrypt | -O2 307, -O1 2, -O0 2 | -Os 307, -O1 2, -O0 2 | a few files on purpose |
| bzip2, expect, giflib, hostname, iptables, lzo, xdgmime | -O2 | -O2 | own -O2 |
| libiri | -O0 | -O0 | own -O0 |

### 2.2 All packages incl. product (from the spec files: explicit `-O` in CFLAGS / CXXFLAGS / optflags)

168 packages (181 spec files) set an explicit `-O`. Limits of this list:
- a `-O` written inside a Makefile or CMakeLists is not covered;
- `%if` branches in the spec are not evaluated, so some entries (marked "check") may only apply to coverage / test builds.

| Level | Packages | Names |
|---|---|---|
| -O2 | 115 | most VD framework / middleware packages with `export CFLAGS="$CFLAGS -O2 ..."` (e.g. avocd, allshare-svc, appdrm, libmm-player, libmm-wfd, net-config, iptables, libave, unidlna-tv, widevine, qte-bm, smack, the 24 com.samsung.dali.* samples, the *-debugmenu libraries) |
| -Og | 21 | tvs-api, tvs-api-native, tvs-chms, tvs-core, tvs-dbms, tvs-dvb-chms, tvs-dvbbase-chms, tvs-ewbs, tvs-ht, tvs-iss, tvs-list-app, tvs-nrt, tvs-util, rct-service, org.tizen.rct-app, ug_rct, reminder-api, reminder-service, org.tizen.reminder, mmi, mmi-plugins-default |
| -O3 | 8 | capi-mva-contextfw, capi-stt-wrapper-tv, capi-tts-wrapper-tv, capi-va-policy-tv, capi-vc-wrapper-tv, capi-voice-source-manager-tv, libogg, libvorbis |
| -O0 | 6 | rpm; check: nnstreamer, machine-learning-api, source-service (coverage), vulkan-utility-libraries, vulkan-validation-layers |
| -O1 / mixed | 4 | lttng-ust (-O1 on purpose), tztv-kernel, chromium-efl (-Os in its own build), escargot |
| -Os (already the LLVM level) | 14 | dali, dali-adaptor, dali-toolkit, dali-extension, dali-ui, dali-csharp-binder, capi-dali-oneui-tv, libheif, lightweight-web-engine, tizen-tools, glibc (static part), the one-ui examples |

Points for HQ's decision:
- **The 21 `-Og` packages** (mainly the TV service tvs-*) are built with debug-level optimisation in both images. This is worth checking with the owners.
- **org.tizen.webserver** sets `-O2` in its spec, but its own make files always add `-O0 -g3 -DDEBUG` (the release flags are commented out). The shipped binaries are therefore unoptimised in both images. This is independent of the compiler and should be confirmed with the owner.
- **The 115 `-O2` packages** do not get the size optimisation of the LLVM image. Whether they should follow `-Os` is a per-package performance / size decision. No change has been made yet, so there is no "after" data. If HQ agrees, we can align a chosen set and measure size and performance on the board.

## 3. LTO

**Overall.** The LLVM image links about the same share of its ELF files with LTO as the GCC image: 5,621 of 13,350, compared with 5,688 of 13,169.

**Exclusion lists in the Clang build.conf.** build.conf keeps three lists:
- `%lto_uncompatible_pkgs`: 71 packages;
- `%lto_armrel32_pkgs`: 58 packages;
- `%lto_pkgs`: 15 packages.

For most of the packages in these lists the LLVM image is smaller: `.text` is 10-35 % below the GCC image, with `-Os` one plausible contributor alongside effective GCC and Clang hardening, ISA and LTO flags. A few grow noticeably and will be analysed one by one:

| Package | List | GCC: LTO ELF / all, .text KB, .dynsym+.dynstr KB | LLVM: same | .text | .dynsym+.dynstr |
|---|---|---|---|---|---|
| avoc-daemon | lto_uncompatible | 3 / 3, 1760, 100 | 3 / 3, 4007, 1356 | +127.7% | +1262.2% |
| org.tizen.stand-by-scan | lto_armrel32 | 0 / 3, 84, 39 | 0 / 3, 281, 194 | +235.6% | +395.3% |
| org.tizen.tv-viewer | lto | 3 / 8, 7391, 3761 | 3 / 8, 10508, 8122 | +42.2% | +116.0% |
| libslive-provider | lto_uncompatible | 0 / 4, 659, 359 | 0 / 4, 1014, 743 | +53.8% | +106.9% |
| ci-module | lto_uncompatible | 2 / 3, 4762, 1471 | 0 / 3, 3540, 3477 | -25.7% | +136.4% |
| ug-ics-efl | lto_uncompatible | 8 / 8, 1693, 70 | 0 / 8, 2110, 111 | +24.6% | +60.2% |
| esg-api | lto_armrel32 | 0 / 2, 193, 43 | 0 / 2, 331, 54 | +71.1% | +25.4% |
| qte-bm | lto_uncompatible | 8 / 14, 9299, 1273 | 8 / 14, 14072, 1269 | +51.3% | -0.3% |

Two of these packages (ci-module and ug-ics-efl) are linked with LTO in the GCC image but not in the LLVM image, although they are in `%lto_uncompatible_pkgs`.

**Packages not in any list that have fewer LTO-linked ELF in the LLVM image (15).** The product packages among them are:
- wpasupplicant: 5 LTO ELF in the GCC image, 1 in the LLVM image;
- libdbuspolicy: 13 → 2;
- libtbb, nsjail, soc-ai-classifier, soc-cpu-heavyload-ewtest, libai-classifier-impl, systemd-boot-helper, ext4-utils, freetype2.

The cause found so far: these packages link with their own link command, which carries no `-flto`. GCC's driver loads its LTO plugin for every link, but clang's driver loaded LLVMgold only when `-flto` was on the link line. The LLVM toolchain has now been changed to behave like GCC (OBS llvm r10, committed 12 Nov). After the next Base rebuild these packages are expected to be linked with LTO as well.

**Effect of LTO alone.** It cannot be separated from `-Os` in this comparison, because both images differ in both. It can be measured with the last LLVM image built before build-wide LTO (20261103.1), if that build is still on the server. The per-file comparison of that measurement will follow.

## 4. Other compilers and toolchains

| Kind | Found | Note |
|---|---|---|
| musl-gcc / musl | none (0 specs, 0 ELF) | - |
| Rust | 163 ELF, the same in both images (appcore-agent, bundle, capi-appfw-*, pkgmgr-server, rpc-port, rust-* crates) | built by rustc (LLVM based), not affected by the GCC → Clang switch |
| Go | 20 ELF (golang 19, sdk-core 1); spec of opengl-es-g52 uses `go build` | built by the Go toolchain |
| Kernel / TEE / driver builds with `CROSS_COMPILE` | 64 specs (tztv-* media drivers, wifi-drivers-*, trustzone-*, sim-module, secure-driver-nvt, acm-modules, ...) | kernel modules and TEE parts, built by the kernel toolchain, outside the user-space switch |
| `_toolchain_override` (GCC forced) | gcc*, glibc, llvm, yaca | yaca: to be reviewed |
| gfortran | gcc and qemu-accel specs | toolchain only |
| aarch64 target in an armv7l build | gst-ffmpeg-atsc3 (2 specs) | to be checked |
| Non-ARM ELF in the armv7l repositories | 4,056 in the LLVM image: mic-bootstrap (1,799), qemu-accel (952), cross-aarch64-gcc (362 + 368), cross-arm-gcc (52), sdk-installer (207), dotnet-build-tools (99), jdk (81) | build-host tools for the image / package build, not installed on the TV |
| Tizen Studio native build (`tizen build-native` / tizen-sdk) | 331 spec files (keyword match) | to be checked |
