# HQ Table — ARM-Generated (A32) Files in the LLVM Image

Nov 20, 2026 · @Hao

With the LTO and PIE image, we updated the data: 609 loadable user-space ELF files are ARM-predominant (A32), out of 5,166 loadable ELF files in 2,342 RPMs. Their estimated A32 code is 359.7 MB. The 211 largest files, listed below, hold 97% of it.

## 1. Analysis

**Why the LLVM image has A32 code.** The armv7l optflags contain `-mthumb` for both compilers. GCC Product builds also got `-mthumb` appended last by the `gcc-warning-build-env` wrapper. That covers a dropped `$CFLAGS` and overrides an explicit `-marm`, so the GCC image was Thumb-2. Clang has no wrapper, and Tizen Clang 22.1.8 without `-mthumb` emits A32 (verified on the GBS compile line: triple `armv7-tizen-linux-gnueabi`, mapping symbol `$a`; with optflags: `thumbv8a`, `$t`). So under Clang a file is A32 when its build drops `$CFLAGS`, passes `-marm`, uses `.arm` / `target("arm")` or A32 assembly, or ships a prebuilt binary.

**Cause by class** (211 largest files, from compiler markers in `.comment`, DWARF producer records and package origin):

| Likely cause | Files | Est. A32 code | Our solution |
| --- | --: | --: | --- |
| Bundled prebuilt (bpftrace, LLVM 19 libs in vd\_memps) | 5 | 129.0 MiB | Supplier Thumb-2 build, or keep out of the release image |
| Clang compile without `-mthumb` (dropped CFLAGS, `-marm` or `.arm`) | 133 | 123.4 MiB | EXP-T1: `clang-force-options` with `-mthumb` |
| GCC-built: prebuilt, assembly or wrapper-exempt | 49 | 29.2 MiB | Per package: source build or supplier Thumb-2 |
| Explicit `-marm` (recorded in DWARF producer: bluetooth-impl-sec-oal, widevine-cdm) | 11 | 26.1 MiB | Remove `-marm` in the package build |
| Prebuilt (argot, argo-tizen CI with cargo-tizen) | 2 | 11.2 MiB | Thumb-2 Rust target from the supplier, then a one-change board test |
| No compiler marker (prebuilt or stripped) | 2 | 9.7 MiB | Supplier Thumb-2 build |
| Base GCC build without the wrapper (glibc; GCC default is A32) | 7 | 3.5 MiB | Add `-mthumb` where not ABI-bound |
| Rust-built, target not verified | 2 | 1.1 MiB | Check the Rust target triple |

**Our solution, EXP-T1.** build.conf preinstalls the Base package `clang-force-options` with `%clang_force_options -mthumb`. During each package build it adds `-mthumb` to `clang.cfg`, and it removes it afterwards. Package exemptions are honored, and an explicit package `-marm` still wins. Kernel and external-module packages are exempt.

**Effect.** The size and memory effect is measured in the EXP-T1 GBS pilot next week (deviced, gst-plugins-dash, inference-engine-tflite), then in a QuickBuild. The measures are A32 share per file, `.text`, PSS of the top media processes, boot time and playback. argot gets its own one-change measurement on KantSU2E. The 133 Clang-class files (123.4 MiB of A32 code) are the direct target of EXP-T1; the prebuilt classes need supplier builds.

## 2. Per-file list (211 largest of 609, by estimated A32 code)

“Code KiB” is the executable code size; “A32 share” is the share of code in ARM mode, from mapping symbols where a symbol table exists, otherwise from the instruction condition-field statistic. …/preload-tpk and …/preload-rw-tpk stand for `/usr/apps/.preload-tpk` and `/usr/apps/.preload-rw-tpk`; `!` marks a file inside a TPK. The 398 smaller files (each under 122 KiB) hold the remaining 3% and follow the same classes.

### Files 1–108

| # | Package | File | Code KiB | A32 share | Est. A32 KiB | Marker | Likely cause |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | vd_memps | `/usr/lib/bpftrace/libLLVM.so.19.1` | 51,120 | 100% | 51,120 | GCC | Bundled prebuilt |
| 2 | vd_memps | `/usr/lib/bpftrace/libclang-cpp.so.19.1` | 48,971 | 100% | 48,971 | GCC | Bundled prebuilt |
| 3 | vd_memps | `/usr/lib/bpftrace/libclang.so.19.1` | 27,554 | 100% | 27,554 | GCC | Bundled prebuilt |
| 4 | nodejs | `/usr/bin/node` | 23,174 | 100% | 23,174 | GCC+Clang | Clang, no -mthumb |
| 5 | bluetooth-impl-sec-oal | `/prd/usr/lib/libbluetooth.so` | 9,979 | 100% | 9,979 | GCC | Explicit -marm |
| 6 | argot | `…/preload-tpk/com.samsung.tizen.argot-0.6.1-armv7l.tpk!bin/argot` | 9,826 | 100% | 9,826 | GCC+Rust | Prebuilt (cargo-tizen) |
| 7 | tvp-tv | `/opt/usr/apps/ieme/Ddrm/libFPS.so` | 8,873 | 100% | 8,873 | none | No marker |
| 8 | gst-ffmpeg | `/usr/local/lib/libavcodec.so` | 8,152 | 100% | 8,152 | GCC+Clang | Clang, no -mthumb |
| 9 | nnstreamer-tensorflow2-lite | `/usr/lib/nnstreamer/filters/libnnstreamer_filter_tensorflow2-lite.so` | 6,223 | 100% | 6,217 | GCC+Clang | Clang, no -mthumb |
| 10 | inference-engine-tflite | `/usr/lib/libinference-engine-tflite.so` | 6,222 | 100% | 6,210 | GCC+Clang | Clang, no -mthumb |
| 11 | libav-common | `/usr/lib/libavcodec_common.so.55.52.102` | 5,050 | 100% | 5,045 | GCC+Clang | Clang, no -mthumb |
| 12 | org.tizen.tv-viewer | `/usr/apps/org.tizen.tv-viewer/bin/tv-viewer` | 4,705 | 97% | 4,583 | GCC+Clang | Clang, no -mthumb |
| 13 | bluetooth-impl-sec-oal | `/prd/usr/lib/libbluetooth_rtk.default.so` | 4,335 | 100% | 4,335 | GCC | Explicit -marm |
| 14 | bluetooth-impl-sec-oal | `/prd/usr/lib/libbluetooth_mtk.default.so` | 4,019 | 100% | 4,019 | GCC | Explicit -marm |
| 15 | vd_memps | `/usr/bin/bpftrace32` | 3,868 | 100% | 3,868 | GCC | Bundled prebuilt |
| 16 | sensor-hal-accelerometer-sensor | `/usr/lib/sensor/libsensor-hal-accelerometer-sensor.so` | 3,923 | 97% | 3,801 | GCC+Clang | Clang, no -mthumb |
| 17 | pisa-service | `…/preload-rw-tpk/com.samsung.tv.pisa-service-31.11.126-arm.tpk!res/awf_for_andy/partner/palsdk/encrypt_addon.tizen.node` | 3,350 | 95% | 3,182 | GCC | GCC prebuilt / asm / exempt |
| 18 | qte-bm | `/usr/lib/BM/qt5.5.1/lib/libQt5Widgets.so.5.5.1` | 2,968 | 100% | 2,968 | GCC+Clang | Clang, no -mthumb |
| 19 | qte-bm | `/usr/lib/BM/qt5.5.1/lib/libQt5Core.so.5.5.1` | 2,709 | 100% | 2,709 | GCC+Clang | Clang, no -mthumb |
| 20 | bluetooth-impl-sec-oal | `/prd/usr/lib/libleaudio.so` | 2,764 | 96% | 2,662 | GCC | Explicit -marm |
| 21 | qte-bm | `/usr/lib/BM/qt5.5.1/lib/libQt5Gui.so.5.5.1` | 2,655 | 100% | 2,655 | GCC+Clang | Clang, no -mthumb |
| 22 | rpm | `/usr/lib/librpm.so.3.1.0` | 2,337 | 100% | 2,335 | GCC+Clang | Clang, no -mthumb |
| 23 | service-enabler | `/var/tmp/ses_dir/.preload-rw-tpk/dev-com.samsung.tizen.knox-matrix-6.0.22-10.0-arm.tpk!lib/libkmx-chain-manager.so` | 2,201 | 100% | 2,201 | GCC | GCC prebuilt / asm / exempt |
| 24 | org.tizen.mbr-daemon | `/usr/bin/mbr-daemon` | 1,735 | 100% | 1,735 | GCC+Clang | Clang, no -mthumb |
| 25 | argot | `/usr/bin/argot` | 1,685 | 100% | 1,685 | GCC+Rust | Prebuilt (cargo-tizen) |
| 26 | com.samsung.tv.slive-daemon | `…/preload-rw-tpk/com.samsung.tv.slive-daemon-2.9.99927-arm.tpk!lib/libavcodec_common.so.55` | 1,754 | 93% | 1,635 | GCC | GCC prebuilt / asm / exempt |
| 27 | ncnn | `/usr/lib/libncnn.so` | 1,529 | 100% | 1,529 | GCC+Clang | Clang, no -mthumb |
| 28 | org.tizen.webserver | `/usr/apps/org.tizen.webserver/bin/liblighttpd.so` | 1,480 | 100% | 1,480 | GCC+Clang | Clang, no -mthumb |
| 29 | pisa-service | `…/preload-rw-tpk/com.samsung.tv.pisa-service-31.11.126-arm.tpk!bin/adagent-service` | 1,489 | 96% | 1,428 | GCC+Clang | Clang, no -mthumb |
| 30 | sys-tools | `/usr/bin/target_view/python3/bin/python3.5m` | 1,541 | 88% | 1,348 | GCC+Clang | Clang, no -mthumb |
| 31 | playready | `/usr/lib/libplayready.so.0.1.0` | 1,514 | 89% | 1,346 | GCC+Clang | Clang, no -mthumb |
| 32 | com.samsung.tv.cobalt-perf | `/usr/apps/com.samsung.tv.cobalt/bin/crashpad_handler` | 1,320 | 100% | 1,320 | GCC | GCC prebuilt / asm / exempt |
| 33 | com.samsung.tv.cobalt-perf | `/usr/apps/com.samsung.tv.cobalt/bin_gold/cobalt_launcher` | 1,314 | 100% | 1,314 | GCC | GCC prebuilt / asm / exempt |
| 34 | com.samsung.tv.cobalt-perf | `/usr/apps/com.samsung.tv.cobalt/bin/cobalt_launcher` | 1,294 | 100% | 1,294 | GCC | GCC prebuilt / asm / exempt |
| 35 | com.samsung.tv.cobalt-perf | `/usr/apps/com.samsung.tv.cobalt/bin_gold/crashpad_handler` | 1,278 | 100% | 1,278 | GCC | GCC prebuilt / asm / exempt |
| 36 | widevine-cdm | `/opt/usr/apps/Ddrm/WidevineCdm/lib/libwvcdmleve3.so.0.1.1` | 2,225 | 56% | 1,235 | GCC+Clang | Explicit -marm |
| 37 | playready-test | `/opt/usr/apps/playready/playready_test` | 1,627 | 75% | 1,225 | GCC+Clang | Clang, no -mthumb |
| 38 | widevine-cdm | `/opt/usr/apps/Ddrm/WidevineCdm/lib/libwvcdm.so.0.1.1` | 2,092 | 58% | 1,224 | GCC+Clang | Explicit -marm |
| 39 | multiprofile-service | `…/preload-rw-tpk/com.samsung.tv.multiprofile-service-126.26.09212-arm.tpk!bin/multiprofile-serviceapp` | 1,255 | 96% | 1,199 | GCC+Clang | Clang, no -mthumb |
| 40 | org.tizen.tts-engine-neural | `…/preload-rw-tpk/org.tizen.tts-engine-neural-27.26.09282-arm.tpk!lib/libSMT_engine_sh.so` | 1,267 | 93% | 1,183 | GCC | GCC prebuilt / asm / exempt |
| 41 | performeter-perf | `/opt/usr/apps/streamline_module/perf/gatord` | 1,218 | 96% | 1,174 | GCC | GCC prebuilt / asm / exempt |
| 42 | com.samsung.tv.ghservice | `…/preload-rw-tpk/com.samsung.tv.ghservice-8.26.09293-arm.tpk!shared/res/libcompgamehome.so` | 1,195 | 97% | 1,159 | GCC+Clang | Clang, no -mthumb |
| 43 | vdfs | `/prd/usr/bin/mkfs.vdfs` | 1,256 | 90% | 1,129 | GCC+Clang | Clang, no -mthumb |
| 44 | vdfs | `/prd/usr/bin/tune.vdfs` | 1,207 | 93% | 1,127 | GCC+Clang | Clang, no -mthumb |
| 45 | vdfs | `/prd/usr/bin/fsck.vdfs` | 1,218 | 93% | 1,128 | GCC+Clang | Clang, no -mthumb |
| 46 | vdfs | `/prd/usr/bin/unpack.vdfs` | 1,206 | 94% | 1,128 | GCC+Clang | Clang, no -mthumb |
| 47 | glibc | `/lib/libc.so.6` | 1,108 | 100% | 1,105 | GCC | Base GCC, no wrapper |
| 48 | glibc | `/lib/libc-2.40_perf.so` | 1,107 | 100% | 1,104 | GCC | Base GCC, no wrapper |
| 49 | com.samsung.tv.vif | `…/preload-rw-tpk/com.samsung.tv.vif-26.09.29271-arm.tpk!bin/voice-interaction-framework` | 1,067 | 96% | 1,019 | none | No marker |
| 50 | bluetooth-impl-sec-oal | `/prd/usr/lib/librtkbt_ss_da.so` | 1,012 | 98% | 992 | GCC | Explicit -marm |
| 51 | com.samsung.tv.utterance-recommender-service | `…/preload-rw-tpk/com.samsung.tv.utterance-recommender-service-1.4.3226-arm.tpk!bin/utterance-recommender-core` | 1,007 | 98% | 991 | GCC+Clang | Clang, no -mthumb |
| 52 | webapi-plugins-avplay | `/usr/lib/tizen-extensions-crosswalk/libwebapis_avplaystore.so` | 991 | 100% | 991 | GCC+Clang | Clang, no -mthumb |
| 53 | nagsam-mw | `/usr/lib/debug_output/libnagsamtvs-api.so` | 983 | 100% | 983 | GCC | GCC prebuilt / asm / exempt |
| 54 | com.samsung.ep-plateau-agent-service | `…/preload-rw-tpk/com.samsung.ep-plateau-agent-service-1.6.2126-arm.tpk!lib/libtvs-api.so` | 983 | 99% | 969 | GCC | GCC prebuilt / asm / exempt |
| 55 | gst-plugins-dash | `/usr/lib/libdash.so` | 962 | 100% | 962 | GCC+Clang | Clang, no -mthumb |
| 56 | performeter-perf | `/opt/usr/apps/streamline_module/perf/non_gpu/gatord` | 992 | 97% | 958 | GCC | GCC prebuilt / asm / exempt |
| 57 | bluetooth-frwk | `/usr/lib/libbluetooth-api.so.1.0.0` | 951 | 100% | 951 | GCC+Clang | Clang, no -mthumb |
| 58 | bluetooth-impl-sec-oal | `/prd/usr/lib/libaudio.a2dp.default.so` | 948 | 100% | 948 | GCC | Explicit -marm |
| 59 | bluetooth-impl-sec-oal | `/prd/usr/lib/libaudio.leaudio.default.so` | 941 | 100% | 941 | GCC | Explicit -marm |
| 60 | webapi-plugins-avplay | `/usr/lib/tizen-extensions-crosswalk/libwebapis_avplay.so` | 917 | 100% | 917 | GCC+Clang | Clang, no -mthumb |
| 61 | com.samsung.tv.slive-daemon | `…/preload-rw-tpk/com.samsung.tv.slive-daemon-2.9.99927-arm.tpk!lib/libtvs-api.so` | 922 | 99% | 913 | GCC | GCC prebuilt / asm / exempt |
| 62 | rust-std-shared | `/usr/lib/libstd-161dbff30b3b0c00.so` | 910 | 100% | 910 | GCC+Rust | Rust, target unverified |
| 63 | org.tizen.dseal | `…/preload-rw-tpk/org.tizen.dseal-1.2.2427-arm.tpk!lib/libtvs-api.so` | 910 | 100% | 910 | GCC | GCC prebuilt / asm / exempt |
| 64 | org.tizen.dseal | `…/preload-rw-tpk/org.tizen.dseal-1.2.2427-arm.tpk!lib/armv7l/libtvs-api.so` | 910 | 98% | 892 | GCC | GCC prebuilt / asm / exempt |
| 65 | libpisa-ipc | `/usr/lib/libpisa-ipc.so` | 880 | 100% | 880 | GCC+Clang | Clang, no -mthumb |
| 66 | org.tizen.ScreenMirroring-app-tv | `…/preload-rw-tpk/org.tizen.ScreenMirroring-app-tv-4.2.09250-arm.tpk!bin/screenmirroring-app-tv` | 949 | 91% | 865 | GCC+Clang | Clang, no -mthumb |
| 67 | webapi-plugins | `/usr/lib/tizen-extensions-crosswalk/libtizen_mediacontroller.so` | 792 | 100% | 792 | GCC+Clang | Clang, no -mthumb |
| 68 | com.samsung.tv.uem-client | `…/preload-tpk/com.samsung.tv.uem-client-1.2.55-arm.tpk!lib/plugin/libiothub_client.so` | 785 | 100% | 785 | GCC | GCC prebuilt / asm / exempt |
| 69 | service-enabler | `/var/tmp/ses_dir/.preload-rw-tpk/dev-com.samsung.tizen.smartthings-plugin-6.0.5-10.0-arm.tpk!lib/libshp.so` | 783 | 100% | 783 | GCC | GCC prebuilt / asm / exempt |
| 70 | cms-service | `…/preload-rw-tpk/com.samsung.tv.cms-service-127.26.09301-arm.tpk!bin/cms-daemon` | 753 | 97% | 729 | GCC+Clang | Clang, no -mthumb |
| 71 | org.tizen.AVControl | `/usr/apps/org.tizen.AVControl/bin/AVControl` | 723 | 100% | 723 | GCC+Clang | Clang, no -mthumb |
| 72 | widevine-cdm-test | `/opt/usr/apps/wvcdm/test_oemcrypto_level3` | 1,275 | 55% | 706 | GCC+Clang | Clang, no -mthumb |
| 73 | widevine-cdm-test | `/opt/usr/apps/wvcdm/test_oemcrypto` | 1,166 | 60% | 696 | GCC+Clang | Clang, no -mthumb |
| 74 | playready-test | `/opt/usr/apps/playready/libplayready.v3test.so.0.1.0` | 809 | 85% | 687 | GCC+Clang | Clang, no -mthumb |
| 75 | playready | `/usr/lib/libplayready3.so.0.1.0` | 830 | 82% | 685 | GCC+Clang | Clang, no -mthumb |
| 76 | com.samsung.tizen.perception-engine | `…/preload-rw-tpk/com.samsung.tizen.perception-engine-1.0.3-arm.tpk!bin/com.samsung.tizen.perception-engine` | 671 | 100% | 671 | GCC+Clang | Clang, no -mthumb |
| 77 | widevine-cdm-test | `/opt/usr/apps/wvcdm/test_wvcdm` | 692 | 96% | 661 | GCC+Clang | Clang, no -mthumb |
| 78 | org.tizen.pvr-service | `/usr/lib/libpvr-service-interface.so` | 682 | 95% | 649 | GCC+Clang | Clang, no -mthumb |
| 79 | gst-ffmpeg | `/usr/local/lib/libavformat.so` | 651 | 100% | 648 | GCC+Clang | Clang, no -mthumb |
| 80 | libgcrypt | `/usr/lib/libgcrypt.so.20.5.0` | 648 | 100% | 647 | GCC+Clang | Clang, no -mthumb |
| 81 | org.tizen.pvr-service | `/usr/bin/pvr-service` | 670 | 95% | 636 | GCC+Clang | Clang, no -mthumb |
| 82 | webapi-plugins | `/usr/lib/tizen-extensions-crosswalk/libtizen_bluetooth.so` | 614 | 100% | 614 | GCC+Clang | Clang, no -mthumb |
| 83 | com.samsung.tv.slive-daemon | `…/preload-rw-tpk/com.samsung.tv.slive-daemon-2.9.99927-arm.tpk!lib/libhls.so` | 610 | 98% | 597 | GCC+Clang | Clang, no -mthumb |
| 84 | gst-ffmpeg-atsc3 | `/usr/lib/gstreamer-1.0/libgstffmpegatsc3.so` | 593 | 100% | 590 | GCC+Clang | Clang, no -mthumb |
| 85 | com.samsung.tv.bmp | `…/preload-rw-tpk/com.samsung.tv.bmp-5.0.45-arm.tpk!bin/bmp` | 603 | 97% | 584 | GCC+Clang | Clang, no -mthumb |
| 86 | vd-capi-network | `/usr/bin/tcpdump` | 573 | 100% | 573 | GCC | GCC prebuilt / asm / exempt |
| 87 | vd_memps | `/usr/lib/bpftrace/libbcc_bpf.so.0` | 551 | 100% | 551 | GCC+Clang | Bundled prebuilt |
| 88 | deviced | `/usr/bin/deviced` | 550 | 100% | 550 | GCC+Clang | Clang, no -mthumb |
| 89 | com.samsung.tv.broadcastingmenu | `/usr/lib/libbroadcastmenu-csharpGadgetSupport.so` | 540 | 100% | 540 | GCC+Clang | Clang, no -mthumb |
| 90 | bluetooth-frwk-service | `/usr/bin/bt-service` | 534 | 100% | 534 | GCC+Clang | Clang, no -mthumb |
| 91 | com.samsung.tv.broadcastingmenu | `/usr/apps/com.samsung.tv.broadcastingmenu/bin/broadcastingmenu` | 532 | 100% | 532 | GCC+Clang | Clang, no -mthumb |
| 92 | glibc | `/sbin/ldconfig` | 512 | 100% | 510 | GCC | Base GCC, no wrapper |
| 93 | org.tizen.volume-app | `/usr/apps/org.tizen.volume-app/bin/volume-app` | 506 | 100% | 506 | GCC+Clang | Clang, no -mthumb |
| 94 | aurum-bootstrap | `/usr/apps/org.tizen.aurum-bootstrap/bin/aurum-bootstrap` | 500 | 100% | 500 | GCC+Clang | Clang, no -mthumb |
| 95 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_kr.so` | 607 | 82% | 499 | GCC | GCC prebuilt / asm / exempt |
| 96 | aurum | `/usr/lib/libaurum.so.0.1.1` | 480 | 100% | 480 | GCC+Clang | Clang, no -mthumb |
| 97 | service-enabler | `/var/tmp/ses_dir/.preload-rw-tpk/dev-com.samsung.tizen.smartthings-plugin-6.0.5-10.0-arm.tpk!lib/libshpplatform.so` | 484 | 97% | 471 | GCC | GCC prebuilt / asm / exempt |
| 98 | gst-ffmpeg | `/usr/local/lib/libswscale.so` | 473 | 100% | 471 | GCC+Clang | Clang, no -mthumb |
| 99 | com.samsung.tv.termsclient | `…/preload-rw-tpk/com.samsung.tv.termsclient-1.2.1127-arm.tpk!bin/termsclient` | 483 | 96% | 466 | GCC+Clang | Clang, no -mthumb |
| 100 | account-extra-service | `…/preload-rw-tpk/com.samsung.tv.account-extra-service-127.26.07311-arm.tpk!bin/account-extra-service` | 479 | 96% | 461 | GCC+Clang | Clang, no -mthumb |
| 101 | webapi-plugins | `/usr/lib/tizen-extensions-crosswalk/libtizen_ml.so` | 451 | 100% | 451 | GCC+Clang | Clang, no -mthumb |
| 102 | wifi-drivers-RTK-rtl8822EU-perf | `/lib/modules/linux/wifi/rtl8822eu/rtwpriv` | 436 | 100% | 436 | GCC | GCC prebuilt / asm / exempt |
| 103 | org.tizen.ssoservice | `…/preload-rw-tpk/org.tizen.ssoservice-127.26.09251-arm.tpk!shared/res/lib/libsa-common-adapter.so` | 463 | 94% | 437 | GCC+Clang | Clang, no -mthumb |
| 104 | libslive-provider | `/usr/apps/org.tizen.slive-util/bin/slive-util` | 433 | 100% | 433 | GCC+Clang | Clang, no -mthumb |
| 105 | streaming-accelerator | `/usr/bin/HttpAccel` | 506 | 82% | 415 | GCC+Clang | Clang, no -mthumb |
| 106 | qte-bm | `/usr/lib/BM/qt5.5.1/lib/libQt5Network.so.5.5.1` | 413 | 100% | 413 | GCC+Clang | Clang, no -mthumb |
| 107 | com.samsung.tv.slive-daemon | `…/preload-rw-tpk/com.samsung.tv.slive-daemon-2.9.99927-arm.tpk!lib/libavformat_mmhls.so.55` | 430 | 94% | 405 | GCC | GCC prebuilt / asm / exempt |
| 108 | gst-plugins-hls | `/usr/lib/libavformat_mmhls.so.55` | 407 | 99% | 404 | GCC+Clang | Clang, no -mthumb |

### Files 109–211

…/crosswalk stands for `/usr/lib/tizen-extensions-crosswalk`.

| # | Package | File | Code KiB | A32 share | Est. A32 KiB | Marker | Likely cause |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- |
| 109 | libav-common | `/usr/lib/libavutil_common.so.52.66.100` | 379 | 99% | 377 | GCC+Clang | Clang, no -mthumb |
| 110 | webapi-plugins | `…/crosswalk/libtizen_iotcon.so` | 376 | 100% | 376 | GCC+Clang | Clang, no -mthumb |
| 111 | bm_graphic_ui | `/usr/lib/BM/JBM/lib/libui-qt_r.so.1.0.0` | 375 | 100% | 375 | GCC | GCC prebuilt / asm / exempt |
| 112 | csft-service | `…/preload-rw-tpk/com.samsung.tv.csft-service-126.26.05071-arm.tpk!bin/csft-daemon` | 387 | 96% | 373 | GCC+Clang | Clang, no -mthumb |
| 113 | boost-test | `/usr/lib/libboost_unit_test_framework.so.1.83.0` | 373 | 100% | 373 | GCC+Clang | Clang, no -mthumb |
| 114 | gst-plugins-dash | `/usr/lib/gstreamer-1.0/libgstdash.so` | 372 | 100% | 371 | GCC+Clang | Clang, no -mthumb |
| 115 | boost-locale | `/usr/lib/libboost_locale.so.1.83.0` | 370 | 100% | 370 | GCC+Clang | Clang, no -mthumb |
| 116 | service-enabler | `/var/tmp/ses_dir/.preload-rw-tpk/dev-com.samsung.tizen.knox-matrix-6.0.22-10.0-arm.tpk!lib/libescrow-vault.so` | 369 | 100% | 369 | GCC | GCC prebuilt / asm / exempt |
| 117 | gst-ffmpeg | `/usr/local/lib/libavutil.so` | 370 | 99% | 368 | GCC+Clang | Clang, no -mthumb |
| 118 | gst-plugins-ss | `/usr/lib/libSSEngine.so` | 366 | 100% | 366 | GCC | GCC prebuilt / asm / exempt |
| 119 | capi-rdm-handler-manager | `/usr/lib/libyaml-cpp.so` | 359 | 100% | 359 | GCC | GCC prebuilt / asm / exempt |
| 120 | remote-server | `/usr/bin/remote-server` | 358 | 100% | 358 | GCC+Clang | Clang, no -mthumb |
| 121 | com.samsung.tv.broadcastingmenu | `/usr/share/menu/providers/libbroadcastmenu-dataprovider.so.0.1` | 347 | 100% | 347 | GCC+Clang | Clang, no -mthumb |
| 122 | com.samsung.tv.ghservice | `…/preload-rw-tpk/com.samsung.tv.ghservice-8.26.09293-arm.tpk!shared/res/libghservice-api.so` | 353 | 98% | 347 | GCC+Clang | Clang, no -mthumb |
| 123 | org.tizen.tts-engine-neural | `…/preload-rw-tpk/org.tizen.tts-engine-neural-27.26.09282-arm.tpk!bin/tts-engine-neural` | 360 | 96% | 346 | GCC+Clang | Clang, no -mthumb |
| 124 | webapi-plugins | `…/crosswalk/libtizen_systeminfo.so` | 342 | 100% | 342 | GCC+Clang | Clang, no -mthumb |
| 125 | libbrotlienc | `/usr/lib/libbrotlienc.so.1.1.0` | 342 | 100% | 342 | GCC+Clang | Clang, no -mthumb |
| 126 | webapi-plugins | `…/crosswalk/libtizen_archive.so` | 333 | 100% | 333 | GCC+Clang | Clang, no -mthumb |
| 127 | com.samsung.tv.coba.adagent | `/usr/apps/.debug-tpk/com.samsung.tv.coba.adagent-26.1.7026.tpk!shared/res/libcomp-adagent.so` | 356 | 94% | 333 | GCC+Clang | Clang, no -mthumb |
| 128 | com.samsung.tv.coba.adagent | `…/preload-rw-tpk/com.samsung.tv.coba.adagent-26.1.7026.tpk!shared/res/libcomp-adagent.so` | 356 | 94% | 333 | GCC+Clang | Clang, no -mthumb |
| 129 | com.samsung.tv.ghdaemon | `…/preload-rw-tpk/com.samsung.tv.ghdaemon-8.26.09301-arm.tpk!bin/ghdaemon` | 332 | 100% | 332 | GCC+Clang | Clang, no -mthumb |
| 130 | gst-plugins-httpdemux | `/usr/lib/libavformat_mmhttp.so.55` | 323 | 99% | 320 | GCC+Clang | Clang, no -mthumb |
| 131 | webapi-plugins | `…/crosswalk/libtizen_filesystem.so` | 316 | 100% | 316 | GCC+Clang | Clang, no -mthumb |
| 132 | gst-plugins-dash | `/usr/lib/libavformat_mmdash.so.55` | 318 | 99% | 315 | GCC+Clang | Clang, no -mthumb |
| 133 | com.samsung.tv.slive-daemon | `…/preload-rw-tpk/com.samsung.tv.slive-daemon-2.9.99927-arm.tpk!lib/libavformat_mmdash.so.55` | 332 | 95% | 314 | GCC | GCC prebuilt / asm / exempt |
| 134 | com.samsung.tv.slive-daemon | `…/preload-rw-tpk/com.samsung.tv.slive-daemon-2.9.99927-arm.tpk!lib/libavformat_mmhttp.so.55` | 331 | 94% | 312 | GCC | GCC prebuilt / asm / exempt |
| 135 | com.samsung.tv.bixbycapsuleviewer | `…/preload-rw-tpk/com.samsung.tv.bixbycapsuleviewer-27.026.07230-arm.tpk!lib/libwebp_lwe.so` | 322 | 95% | 307 | GCC | GCC prebuilt / asm / exempt |
| 136 | glibc | `/usr/sbin/glibc_post_upgrade` | 308 | 98% | 301 | GCC | Base GCC, no wrapper |
| 137 | webapi-network-pepper-plugin | `…/crosswalk/libwebapis_network.so` | 297 | 100% | 297 | GCC+Clang | Clang, no -mthumb |
| 138 | webapi-plugins | `…/crosswalk/libtizen_common.so` | 283 | 100% | 283 | GCC+Clang | Clang, no -mthumb |
| 139 | org.tizen.tv.ci-app | `/usr/lib/libciapp-provider.so` | 272 | 100% | 272 | GCC+Clang | Clang, no -mthumb |
| 140 | com.samsung.tv.broadcastingmenu | `/usr/share/menu/providers/libbroadcastmenu-enablechecker.so.0.1` | 265 | 100% | 265 | GCC+Clang | Clang, no -mthumb |
| 141 | com.samsung.tv.broadcastingmenu | `/usr/share/menu/providers/libbroadcastmenu-visiblechecker.so.0.1` | 260 | 100% | 260 | GCC+Clang | Clang, no -mthumb |
| 142 | sys-tools | `/usr/local/bin/alsan` | 261 | 99% | 259 | GCC+Clang | Clang, no -mthumb |
| 143 | pkgmgr-server | `/usr/bin/pkgmgr-server` | 255 | 100% | 255 | GCC+Rust | Rust, target unverified |
| 144 | sys-tools | `/usr/local/bin/memleak` | 254 | 99% | 252 | GCC+Clang | Clang, no -mthumb |
| 145 | org.tizen.voice-client | `…/preload-rw-tpk/org.tizen.voice-client-26.27.09281-arm.tpk!lib/libFarfield_VAD_TV.so` | 269 | 91% | 244 | GCC | GCC prebuilt / asm / exempt |
| 146 | com.samsung.tv.uem-client | `…/preload-tpk/com.samsung.tv.uem-client-1.2.55-arm.tpk!lib/plugin/libcurl-d.so` | 243 | 100% | 243 | GCC | GCC prebuilt / asm / exempt |
| 147 | sys-tools | `/usr/local/bin/futexctn` | 245 | 99% | 243 | GCC+Clang | Clang, no -mthumb |
| 148 | webapi-plugins | `…/crosswalk/libtizen_application.so` | 237 | 100% | 237 | GCC+Clang | Clang, no -mthumb |
| 149 | pisa-service | `…/preload-rw-tpk/com.samsung.tv.pisa-service-31.11.126-arm.tpk!bin/pisa-service` | 242 | 96% | 233 | GCC+Clang | Clang, no -mthumb |
| 150 | capi-multiprofile-tv | `/usr/lib/libmultiprofile-mapi.so.1.0.0` | 221 | 100% | 221 | GCC+Clang | Clang, no -mthumb |
| 151 | com.samsung.tv.slive-daemon | `…/preload-rw-tpk/com.samsung.tv.slive-daemon-2.9.99927-arm.tpk!lib/libavutil_common.so.52` | 226 | 98% | 221 | GCC | GCC prebuilt / asm / exempt |
| 152 | webapi-tvs-plugin | `…/crosswalk/libwebapis_tvs.so` | 219 | 100% | 219 | GCC+Clang | Clang, no -mthumb |
| 153 | webapi-plugins | `…/crosswalk/libtizen_content.so` | 214 | 100% | 214 | GCC+Clang | Clang, no -mthumb |
| 154 | vd-capi-network | `/usr/bin/iperf` | 213 | 100% | 213 | GCC | GCC prebuilt / asm / exempt |
| 155 | org.tizen.tv-viewer | `/usr/apps/org.tizen.tv-viewer/bin/tvcontrol-notify-manager` | 213 | 100% | 213 | GCC+Clang | Clang, no -mthumb |
| 156 | unzip | `/usr/bin/zipinfo` | 226 | 94% | 212 | GCC+Clang | Clang, no -mthumb |
| 157 | dbus-libs-extension-kdbus | `/usr/lib/libdbus-1.so.3.19.13.extension-kdbus` | 211 | 100% | 211 | GCC+Clang | Clang, no -mthumb |
| 158 | boost-regex | `/usr/lib/libboost_regex.so.1.83.0` | 208 | 100% | 208 | GCC+Clang | Clang, no -mthumb |
| 159 | glibc | `/usr/bin/localedef` | 208 | 100% | 208 | GCC | Base GCC, no wrapper |
| 160 | bluetooth-impl-sec-oal | `/prd/usr/lib/libbt-vendor-aic.so` | 207 | 100% | 207 | GCC | Explicit -marm |
| 161 | eden-webapi-plugins | `…/crosswalk/libwebapis_common.so` | 195 | 100% | 195 | GCC+Clang | Clang, no -mthumb |
| 162 | sys-tools | `/usr/bin/target_view/python3/lib/python3.5/lib-dynload/_decimal.cpython-35m-arm-linux-gnueabi.so` | 209 | 93% | 194 | GCC+Clang | Clang, no -mthumb |
| 163 | org.tizen.voice-client | `…/preload-rw-tpk/org.tizen.voice-client-26.27.09281-arm.tpk!lib/libcapi-context-engine.so` | 194 | 100% | 194 | GCC | GCC prebuilt / asm / exempt |
| 164 | SZDrv_tools | `/sbin/mkfs.szdrv` | 195 | 99% | 194 | GCC+Clang | Clang, no -mthumb |
| 165 | qte-bm | `/usr/lib/BM/qt5.5.1/lib/libQt5Xml.so.5.5.1` | 193 | 100% | 193 | GCC+Clang | Clang, no -mthumb |
| 166 | gstreamer-plugins-pvr | `/usr/lib/gstreamer-1.0/libgstpvrplugin.so` | 197 | 98% | 194 | GCC+Clang | Clang, no -mthumb |
| 167 | SZDrv_tools | `/sbin/fsck.szdrv` | 194 | 99% | 193 | GCC+Clang | Clang, no -mthumb |
| 168 | org.tizen.rdm-client | `/usr/apps/org.tizen.rdm-client/lib/libnats.so` | 188 | 100% | 188 | GCC | GCC prebuilt / asm / exempt |
| 169 | org.tizen.rdm-client | `/usr/apps/org.tizen.rdm-client/lib/libnats.so.2.3` | 188 | 100% | 188 | GCC | GCC prebuilt / asm / exempt |
| 170 | org.tizen.rdm-client | `/usr/apps/org.tizen.rdm-client/lib/libnats.so.2.3.0` | 188 | 100% | 188 | GCC | GCC prebuilt / asm / exempt |
| 171 | webapi-plugins | `…/crosswalk/libtizen_exif.so` | 182 | 100% | 182 | GCC+Clang | Clang, no -mthumb |
| 172 | dbus-libs | `/usr/lib/libdbus-1.so.3.19.13` | 180 | 100% | 180 | GCC+Clang | Clang, no -mthumb |
| 173 | org.tizen.voice-client | `…/preload-rw-tpk/org.tizen.voice-client-26.27.09281-arm.tpk!lib/libTitleSelection.so` | 182 | 96% | 175 | GCC | GCC prebuilt / asm / exempt |
| 174 | glibc | `/lib/libm.so.6` | 182 | 96% | 174 | GCC | Base GCC, no wrapper |
| 175 | webapi-bixby-plugin | `…/crosswalk/libwebapis_bixby.so` | 165 | 100% | 165 | GCC+Clang | Clang, no -mthumb |
| 176 | webapi-unipicture-plugin | `…/crosswalk/libwebapis_unipicture.so` | 160 | 100% | 160 | GCC+Clang | Clang, no -mthumb |
| 177 | com.samsung.tv.kmx-setting-app | `…/preload-rw-tpk/com.samsung.tv.kmx-setting-app-3.10.14-arm.tpk!bin/kmx-setting-app` | 159 | 100% | 159 | GCC+Clang | Clang, no -mthumb |
| 178 | webapi-allshare-pepper-plugin | `…/crosswalk/libwebapis_allshare.so` | 157 | 100% | 157 | GCC+Clang | Clang, no -mthumb |
| 179 | rpm | `/usr/lib/librpmbuild.so.3.1.0` | 153 | 100% | 153 | GCC+Clang | Clang, no -mthumb |
| 180 | cordova-api | `…/crosswalk/libtizen_cordova_globalization.so` | 153 | 100% | 153 | GCC+Clang | Clang, no -mthumb |
| 181 | rpm | `/usr/lib/librpmio.so.3.1.0` | 152 | 99% | 150 | GCC+Clang | Clang, no -mthumb |
| 182 | boost-program-options | `/usr/lib/libboost_program_options.so.1.83.0` | 149 | 100% | 149 | GCC+Clang | Clang, no -mthumb |
| 183 | webapi-plugins | `…/crosswalk/libtizen_tvchannel.so` | 149 | 100% | 149 | GCC+Clang | Clang, no -mthumb |
| 184 | libdeviced | `/usr/lib/libdeviced.so.1.0.3` | 148 | 100% | 148 | GCC+Clang | Clang, no -mthumb |
| 185 | com.samsung.tv.uem-client | `…/preload-tpk/com.samsung.tv.uem-client-1.2.55-arm.tpk!lib/plugin/libXioSdk.so` | 148 | 100% | 148 | GCC | GCC prebuilt / asm / exempt |
| 186 | webapi-pluginmanager-pepper-plugin | `…/crosswalk/libwebapis_PluginManager.so` | 147 | 100% | 147 | GCC+Clang | Clang, no -mthumb |
| 187 | qte-bm | `/usr/lib/BM/qt5.5.1/plugins/platforms/libqlinuxfb.so` | 146 | 100% | 146 | GCC+Clang | Clang, no -mthumb |
| 188 | webapi-systemcontrol-pepper-plugin | `…/crosswalk/libwebapis_systemcontrol.so` | 146 | 100% | 146 | GCC+Clang | Clang, no -mthumb |
| 189 | webapi-broadcast-pepper-plugin | `…/crosswalk/libwebapis_broadcast.so` | 144 | 100% | 144 | GCC+Clang | Clang, no -mthumb |
| 190 | qte-bm | `/usr/lib/BM/qt5.5.1/lib/libQt5Sql.so.5.5.1` | 144 | 100% | 144 | GCC+Clang | Clang, no -mthumb |
| 191 | aurum | `/usr/lib/libaurumsharp.so.0.1.1` | 142 | 100% | 142 | GCC+Clang | Clang, no -mthumb |
| 192 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_fr.so` | 153 | 93% | 142 | GCC | GCC prebuilt / asm / exempt |
| 193 | libwidget_viewer_dali | `/usr/lib/libwidget_viewer_dali.so.1.4.12` | 137 | 100% | 137 | GCC+Clang | Clang, no -mthumb |
| 194 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_ge.so` | 146 | 93% | 136 | GCC | GCC prebuilt / asm / exempt |
| 195 | bluetooth-impl-sec-oal | `/prd/usr/lib/librtkbt_vendor.so` | 136 | 100% | 136 | GCC | Explicit -marm |
| 196 | sys-tools | `/usr/bin/target_view/python3/lib/python3.5/lib-dynload/pyexpat.cpython-35m-arm-linux-gnueabi.so` | 160 | 85% | 136 | GCC+Clang | Clang, no -mthumb |
| 197 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_usen.so` | 144 | 93% | 134 | GCC | GCC prebuilt / asm / exempt |
| 198 | pkgmgr-installer | `/usr/lib/libpkgmgr_installer.so.0.23.4` | 134 | 100% | 134 | GCC+Clang | Clang, no -mthumb |
| 199 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_uken.so` | 144 | 93% | 134 | GCC | GCC prebuilt / asm / exempt |
| 200 | org.tizen.contents-recognition-api | `/usr/lib/libcontents-recognition-api.so.1.0.0` | 134 | 100% | 134 | GCC+Clang | Clang, no -mthumb |
| 201 | gst-plugins-dash | `/usr/lib/libgurl.so` | 134 | 100% | 134 | GCC+Clang | Clang, no -mthumb |
| 202 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_es.so` | 143 | 93% | 133 | GCC | GCC prebuilt / asm / exempt |
| 203 | glibc | `/lib/ld-linux.so.3` | 134 | 98% | 132 | GCC | Base GCC, no wrapper |
| 204 | atsc3uhdcp | `/usr/apps/atsc3uhdcp/digicap/copp/image/client/dpc_D_S01028.csw` | 133 | 99% | 132 | GCC | GCC prebuilt / asm / exempt |
| 205 | luabind | `/usr/lib/libluabindd.so.0.9.0` | 130 | 100% | 130 | GCC+Clang | Clang, no -mthumb |
| 206 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_it.so` | 139 | 93% | 130 | GCC | GCC prebuilt / asm / exempt |
| 207 | pisa-service | `…/preload-rw-tpk/com.samsung.tv.pisa-service-31.11.126-arm.tpk!lib/libpisa-framework.so` | 127 | 98% | 124 | GCC | GCC prebuilt / asm / exempt |
| 208 | app2usb-plugin-tv | `/usr/bin/app2sd-server` | 124 | 100% | 124 | GCC+Clang | Clang, no -mthumb |
| 209 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_pt.so` | 132 | 93% | 123 | GCC | GCC prebuilt / asm / exempt |
| 210 | org.tizen.tts-resource | `…/preload-rw-tpk/org.tizen.tts-resource-26.25.10110-arm.tpk!shared/Lib/libSMT_lang_ru.so` | 132 | 93% | 123 | GCC | GCC prebuilt / asm / exempt |
| 211 | org.tizen.stand-by-scan | `/usr/lib/libstand-by-scan-lib.so` | 122 | 100% | 122 | GCC+Clang | Clang, no -mthumb |
Source: ELF mode scan of all 2,342 RPMs of the LTO and PIE image (QuickBuild 37627297), 18 Nov 2026. “Likely cause” comes from compiler markers, DWARF producer records and package origin. The per-file compile command is confirmed in the EXP-T1 pilot and the sample rebuilds.
