# HQ Table — Packages Built with GCC / G++ in the LLVM Image

Nov 20, 2026 · @Hao

101 packages still contained GCC-built ELF files in the LLVM image. 27 had `gcc` / `g++` hard-coded in a Makefile, CMakeLists or spec. They now take the build environment's `CC` / `CXX`. Of these, 15 have a matched size comparison: 8 are smaller under Clang (−0.7% to −21.5%), 1 is the same (org.tizen.webserver) and 6 are larger (+5.1% to +142.3%) and are analyzed before a decision. The rest are toolchain by design (glibc, gcc, binutils), cross tools not installed on the TV, prebuilt or vendor binaries, or partly GCC.

Two things changed this week. First, the GCC image's `.text` was built at an effective `-O2` with Thumb-2 forced by the `gcc-warning-build-env` wrapper, and the LLVM build is `-Os`. Second, SERET-UL inside tztv-kernel is built by GCC with `-marm`; it is reviewed against the scope rule.

## Per-package list

| # | Package | GCC Base CL | LLVM fix CL | GCC image → LLVM (.text) | Build / runtime | Decision |
| --: | --- | --- | --- | --- | --- | --- |
| 1 | boot-sound | 14220511 | 14448478 | 2 ELF, 217 KB → LLVM image 20261112.1: 2 ELF (all Clang), 171 KB (−21.5%) | Build OK; in image 20261112.1; runtime test pending | Clang smaller; adopt after runtime test |
| 2 | libtv-player | 14297443 | 14448588 | 3 ELF, 1,284 KB → LLVM image 20261112.1: 3 ELF (all Clang), 1,157 KB (−9.9%) | Build OK; in image 20261112.1; runtime test pending | Clang smaller; adopt after runtime test |
| 3 | ppi-display-control | 14233516 | 14448500 | 2 ELF, 43 KB → LLVM image 20261112.1: 2 ELF (all Clang), 49 KB (+15.9%) | Build OK; in image 20261112.1; runtime test pending | Clang larger; decide after runtime / performance test |
| 4 | request-support | 14247519 | 14448576 | Clang build verified; size with next QuickBuild | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 5 | remote-management | 14278376 | 14448314 | Clang build verified; size with next QuickBuild | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 6 | smarthub-connection-test | 14291540 | 14448485 | Clang build verified; size with next QuickBuild | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 7 | display-control-impl-sec | 14233516 | 14448571 | Not in GCC image under this name → Clang: 2 ELF, 17 KB | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 8 | org.tizen.UsbSyncDisplay | 14262074 | 14448681 | Not in GCC image under this name → Clang: 9 ELF, 1,048 KB | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 9 | capi-mva-contextfw | 13738558 | 14448652 | Not in GCC image under this name → Clang: 2 ELF, 40 KB | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 10 | capi-stt-wrapper-tv | 14231451 | 14448672 | Not in GCC image under this name → Clang: 2 ELF, 84 KB | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 11 | capi-va-policy-tv | 14157547 | 14448655 | Not in GCC image under this name → Clang: 1 ELF, 38 KB | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 12 | capi-voice-source-manager-tv | 13738558 | 14448674 | Not in GCC image under this name → Clang: 2 ELF, 40 KB | Build OK (QB conditions); runtime test pending | Size and runtime test |
| 13 | SZDrv\_tools | 11438397 | 14448692 | 2 ELF, 370 KB → Clang: 2 ELF, 389 KB (+5.1%) | Build OK (QB conditions); runtime test pending | Clang larger; decide after runtime / performance test |
| 14 | nvt-pba-interface | 14268942 | 14448696 | 1 ELF, 77 KB → Clang: 1 ELF, 76 KB (−1.3%) | Build OK (QB conditions); runtime test pending | Clang smaller; adopt after runtime test |
| 15 | vdlinux-usb-modules | 14267825 | 14448698 | 2 ELF, 1 KB → Clang: 1 ELF, 1 KB (ELF count differs) | Build OK (QB conditions); runtime test pending | Compare on image, then runtime test |
| 16 | streaming-accelerator | 13165389 | 14448705 | 3 ELF, 525 KB → Clang: 3 ELF, 516 KB (−1.7%) | Build OK (QB conditions); runtime test pending | Clang smaller; adopt after runtime test |
| 17 | feature-config-daemon | 13733507 | 14448709 | 3 ELF, 182 KB → Clang: 3 ELF, 213 KB (+17.0%) | Build OK (QB conditions); runtime test pending | Clang larger; decide after runtime / performance test |
| 18 | mdnsresponder | 13747715 | 14450591 | 3 ELF, 198 KB → Clang: 3 ELF, 254 KB (+28.3%) | Build OK (QB conditions); runtime test pending | Clang much larger; analyze before deciding |
| 19 | libav-common | 14062264 | 14450650 | 3 ELF, 5,586 KB → Clang: 3 ELF, 5,547 KB (−0.7%) | Build OK (QB conditions); runtime test pending | Same size; adopt after runtime test |
| 20 | gst-plugins-httpdemux | 14085831 | 14451112 | 5 ELF, 764 KB → Clang: 3 ELF, 388 KB (ELF count differs) | Build OK (QB conditions); runtime test pending | Compare on image, then runtime test |
| 21 | luabind | 12912787 | 14452018 | 2 ELF, 328 KB → Clang: 2 ELF, 275 KB (−16.2%) | Build OK (QB conditions); runtime test pending | Clang smaller; adopt after runtime test |
| 22 | soc-ir-interface | 13688992 | 14452133 | 2 ELF, 26 KB → Clang: 2 ELF, 63 KB (+142.3%) | Build OK (QB conditions); runtime test pending | Clang much larger; analyze before deciding |
| 23 | lib-ndp-pq-interface-tv | 14258004 | 14452243 | 1 ELF, 79 KB → Clang: 1 ELF, 89 KB (+12.7%) | Build OK (QB conditions); runtime test pending | Clang larger; decide after runtime / performance test |
| 24 | soc\_vendor-user-bins | 12927034 | 14452503 | 7 ELF, 147 KB → Clang: 7 ELF (6 Clang, 1 prebuilt GCC), 126 KB (−14.3%) | Build OK (QB conditions); runtime test pending | Clang smaller; adopt after runtime test |
| 25 | gst-plugins-dash | 14274649 | 14452597 | 9 ELF, 3,737 KB → Clang: 5 ELF, 1,866 KB (ELF count differs) | Build OK (QB conditions); runtime test pending | Compare on image, then runtime test |
| 26 | iotivity | 12913071 | 14452627 | 20 ELF, 2,133 KB → Clang: 20 ELF, 1,750 KB (−18.0%) | Build OK (QB conditions); runtime test pending | Clang smaller; adopt after runtime test |
| 27 | org.tizen.webserver | 14131900 | 14452802 | 4 ELF, 1,691,076 B → Clang: 4 ELF, 1,694,168 B (+0.2%); `-O0` in both (make files add debug flags) | Build OK (QB conditions); runtime test pending | Same size; adopt after runtime test |
| 28 | gst-plugins-atsc3 | 14297461 | In progress (built through cosmos.sh) | 19 of 20 ELF GCC-built | — | Fix in progress |
| 29 | rust | Base | — | 1 of 1 ELF GCC-built | — | Keep: cross / development tool |
| 30 | vd\_memps | 14297850 | — | 7 of 11 ELF GCC-built (bundled bpftrace) | — | Prebuilt bundle; supplier |
| 31 | gcc-riscv64 | Base | — | 22 of 22 | — | Keep GCC: toolchain |
| 32 | gcc-aarch64 | Base | — | 22 of 22 | — | Keep GCC: toolchain |
| 33 | sdk-core | Base | — | 8 of 8 | — | Keep: cross / development tool |
| 34 | gcc | Base | — | 41 of 41 | — | Keep GCC: toolchain |
| 35 | gcc-armv7hl | Base | — | 22 of 22 | — | Keep GCC: toolchain |
| 36 | lib-opengl-es-g52-tv | Image repository only | — | 5 of 5 | — | Prebuilt / vendor; check source build |
| 37 | chromium-efl | 14298789 | — | 19 of 19 | — | Prebuilt / vendor; check source build |
| 38 | bluetooth-impl-sec | 14296634 | — | 16 of 24 | — | Not evaluated yet |
| 39 | qte-bm | 13332532 | — | 1 of 14 | — | Not evaluated yet |
| 40 | native-home | 14271936 | — | 4 of 32 | — | Not evaluated yet |
| 41 | hal-rootstrap | 13416290 | — | 286 of 370 | — | Not evaluated yet |
| 42 | nagsam-mw | 14290200 | — | 3 of 34 | — | Not evaluated yet |
| 43 | com.samsung.tv.cobalt | 14162570 | — | 12 of 12 | — | Prebuilt / vendor; check source build |
| 44 | binutils | Base | — | 35 of 35 | — | Keep GCC: toolchain |
| 45 | tvp-tv | 14280549 | — | 1 of 7 | — | Not evaluated yet |
| 46 | efl | 14296491 | — | 2 of 106 | — | Not evaluated yet |
| 47 | tztv-kernel | 14293732 | — | 5 of 18 (includes GCC-built SERET-UL) | — | Scope review: GCC-only or migration candidate |
| 48 | binutils-aarch64 | Base | — | 29 of 29 | — | Keep: cross / development tool |
| 49 | nnstreamer | 13120874 | — | 1 of 23 | — | Not evaluated yet |
| 50 | binutils-armv7hl | Base | — | 29 of 29 | — | Keep: cross / development tool |
| 51 | gdb | Base | — | 3 of 3 | — | Keep: cross / development tool |
| 52 | org.tizen.tts-engine-neural | 14292417 | 14396892 (Tizen SDK switch) | 19 of 22; with TPK: 28 ELF, 7 Clang, 21 GCC-only | — | Switched to Clang; remaining GCC-only ELF to analyze (prebuilt or built outside build-native) |
| 53 | python3-base | Base | — | 1 of 76 | — | Not evaluated yet |
| 54 | glibc | Base | — | 44 of 44 | — | Keep GCC: toolchain |
| 55 | trustzone-tee-base | 14240399 | — | 28 of 28 | — | Prebuilt / vendor; check source build |
| 56 | trustzone-tee | 14290316 | — | 19 of 23 | — | Not evaluated yet |
| 57 | binutils-riscv64 | Base | — | 26 of 26 | — | Keep: cross / development tool |
| 58 | gst-plugins-hls | 14085831 | — | 1 of 9 | — | Not evaluated yet |
| 59 | performeter | 14032578 | — | 2 of 2 | — | Prebuilt / vendor; check source build |
| 60 | icu | Base | — | 1 of 27 | — | Not evaluated yet |
| 61 | org.tizen.easysetup-daemon | 14293934 | 14391347 (Tizen SDK switch) | 3 of 4; with TPK: 8 ELF, 2 Clang, 6 GCC-only | — | Switched to Clang; remaining GCC-only ELF to analyze |
| 62 | soc-driver-test | 14217134 | — | 1 of 1 | — | Not evaluated yet |
| 63 | wifi-drivers-RTK | 14091856 | — | 3 of 3 | — | Prebuilt / vendor; check source build |
| 64 | wifi-drivers-MTK | 14293507 | — | 12 of 12 | — | Prebuilt / vendor; check source build |
| 65 | trustzone\_ext | 14176624 | — | 2 of 7 | — | Not evaluated yet |
| 66 | vd-capi-network | 14210574 | — | 2 of 8 | — | Not evaluated yet |
| 67 | com.samsung.tv.hfp-agent | 14241645 | — | 1 of 3 | — | Not evaluated yet |
| 68 | knox-browser-tv-api | 14105851 | — | 2 of 7 | — | Not evaluated yet |
| 69 | gst-plugins-ss | 14173949 | — | 3 of 5 | — | Not evaluated yet |
| 70 | org.tizen.rdm-client | 13538969 | — | 3 of 4 | — | Not evaluated yet |
| 71 | yaca | 13336174 | — | 21 of 21 | — | GCC forced in the spec; review |
| 72 | capi-mde-framework-tv | 13352756 | — | 1 of 2 | — | Not evaluated yet |
| 73 | com.samsung.tv.theme-resource | 14299042 | — | 1 of 1 | — | Prebuilt / vendor; check source build |
| 74 | push | 14262750 | — | 1 of 4 | — | Not evaluated yet |
| 75 | M90SF\_builtinCamera-FW-Update | 13261131 | — | 1 of 1 | — | Prebuilt / vendor; check source build |
| 76 | atsc3uhdcp | 14251200 | — | 3 of 11 | — | Not evaluated yet |
| 77 | com.samsung.tv.contentimageapp | 13575147 | — | 1 of 1 | — | Prebuilt / vendor; check source build |
| 78 | capi-rdm-handler-manager | 13446110 | — | 1 of 3 | — | Not evaluated yet |
| 79 | vdtools | 11438397 | — | 3 of 4 | — | Not evaluated yet |
| 80 | bm\_graphic\_ui | 13634671 | — | 1 of 2 | — | Not evaluated yet |
| 81 | e-mod-tizen-virtualscreen-tv | 14262918 | — | 1 of 2 | — | Not evaluated yet |
| 82 | usb-modeswitch | 11438397 | — | 2 of 2 | — | Prebuilt / vendor; check source build |
| 83 | vdprelink | Base | — | 2 of 2 | — | Keep GCC: toolchain |
| 84 | iptables | Base | — | 1 of 117 | — | Not evaluated yet |
| 85 | ppp | 11438397 | — | 2 of 2 | — | Prebuilt / vendor; check source build |
| 86 | camera-device-manager | 14294444 | — | 1 of 5 | — | Not evaluated yet |
| 87 | hal-backend-camera-mobile | 14265510 | — | 1 of 3 | — | Not evaluated yet |
| 88 | contextengine-plugin-smartthings | 14341337 | 14396920 (Tizen SDK switch) | 1 of 3; with TPK: 5 ELF, 4 Clang, 1 GCC-only | — | Switched to Clang; remaining GCC-only ELF to analyze |
| 89 | ug-Network\_StatusUG-efl | 14147520 | — | 1 of 3 | — | Not evaluated yet |
| 90 | e-mod-tizen-wm-policy | 14223799 | — | 1 of 2 | — | Not evaluated yet |
| 91 | e-mod-tizen-keyrouter-tv | 14288387 | — | 1 of 2 | — | Not evaluated yet |
| 92 | org.tizen.menu | 14295788 | — | 2 of 2 | — | Not evaluated yet |
| 93 | gst-plugins-mmhttp | 14173949 | — | 1 of 3 | — | Not evaluated yet |
| 94 | com.samsung.tv.uem-client | 14297054 | 14395463 (Tizen SDK switch) | 1 of 1; with TPK: 7 ELF, 1 Clang, 5 GCC-only | — | Switched to Clang; remaining GCC-only ELF to analyze |
| 95 | soc-mic-ewtest | 13245525 | — | 3 of 3 | — | Not evaluated yet |
| 96 | couponpromotion-pepper-plugin | 13423902 | — | 1 of 1 | — | Not evaluated yet |
| 97 | e-mod-tizen-tvs-helper-tv | 14034648 | — | 1 of 2 | — | Not evaluated yet |
| 98 | SlimFitCam-FW-Update | 12912787 | — | 1 of 1 | — | Prebuilt / vendor; check source build |
| 99 | SlimFitCam4k-FW-Update | 12912787 | — | 1 of 1 | — | Prebuilt / vendor; check source build |
| 100 | service-enabler | 14129402 | — | 2 of 2 | — | Not evaluated yet |
| 101 | onboot-nvt | 14289513 | — | 9 of 9 | — | Prebuilt / vendor; check source build |

Rows 28–101 give “GCC-built ELF / all ELF” in the LLVM image 20261112.1. Size comparison source: GCC image Base 20260916.1 + Product 20261001.3 vs LLVM image 20261112.1 or a local Clang build under QuickBuild conditions.
