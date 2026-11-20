# HQ Table — LTO Enablement

Nov 20, 2026 · @Hao

80 packages were built without LTO by GCC and are still built without LTO by LLVM, because they are in the Clang build.conf exclusion lists. They were put in those lists because of known LTO limitations in the GCC build. For each one we check whether LLVM LTO builds and runs correctly before removing it from the list. This table covers only the packages in the three exclusion lists; it is not every ELF without LTO. Image-wide, 5,621 of 13,350 ELF files are LTO-linked in the LLVM image (GCC: 5,688 of 13,169). Four were already moved to LTO in build.conf@14452507, with a measured `.text` reduction of 0.3% to 11.3% (−1,379,302 B, −7.2% for the four). Packages that GCC linked with LTO but LLVM does not are bugs to fix, not optimization. They are listed separately in section 2.

## 1. LTO enablement candidates (80 packages)

“LTO ELF / all” counts the package's ELF files linked with LTO. “LLVM vs GCC” compares `.text` with both builds without LTO (GCC at the forced `-O2`, LLVM at `-Os`). The last measured column is the LTO effect alone: the same source revision with LTO excluded vs LTO on.

| # | Package | Exclusion list | GCC: LTO ELF / all, .text KB | LLVM: LTO ELF / all, .text KB | LLVM vs GCC .text | Measured LTO on vs off (same source) | Status |
| ---: | --- | --- | --- | --- | ---: | --- | --- |
| 1 | liballshare-core | `%lto_uncompatible_pkgs` | 0/7, 3,511 | 0/7, 2,289 | -34.8% | 1,355,828 → 1,221,288 B (−9.9%) | LTO enabled in build.conf@14452507 |
| 2 | nagsam-mw | `%lto_uncompatible_pkgs` | 0/34, 13,486 | 0/34, 10,705 | -20.6% | 4,239,066 → 4,170,896 B (−1.6%) | LTO enabled in build.conf@14452507 |
| 3 | org.tizen.tv.swu | `%lto_uncompatible_pkgs` | 0/26, 23,381 | 0/26, 16,485 | -29.5% | 10,365,020 → 9,197,846 B (−11.3%) | LTO enabled in build.conf@14452507 |
| 4 | ug-hbbtv-efl | `%lto_uncompatible_pkgs` | 0/12, 4,856 | 0/12, 3,464 | -28.7% | 3,284,182 → 3,274,764 B (−0.3%) | LTO enabled in build.conf@14452507 |
| 5 | acm-core | `%lto_uncompatible_pkgs` | 0/8, 1,515 | 0/8, 1,281 | -15.4% | — | LTO on/off to be measured |
| 6 | alsa-lib | `%lto_uncompatible_pkgs` | 0/1, 372 | 0/1, 326 | -12.4% | — | LTO on/off to be measured |
| 7 | antimalware | `%lto_uncompatible_pkgs` | 0/2, 588 | 0/2, 455 | -22.6% | — | LTO on/off to be measured |
| 8 | atsc3uhdcp | `%lto_uncompatible_pkgs` | 0/11, 464 | 0/11, 438 | -5.6% | — | LTO on/off to be measured |
| 9 | bixby-native-api | `%lto_armrel32_pkgs` | 0/2, 63 | 0/2, 48 | -23.8% | — | LTO on/off to be measured |
| 10 | capi-appfw-app-context-manager | `%lto_uncompatible_pkgs` | 0/3, 49 | 0/3, 39 | -20.4% | — | LTO on/off to be measured |
| 11 | capi-billing-api-internal-tv | `%lto_armrel32_pkgs` | 0/2, 36 | 0/2, 36 | +0.0% | — | LTO on/off to be measured |
| 12 | capi-billing-api-tv | `%lto_armrel32_pkgs` | 0/2, 48 | 0/2, 47 | -2.1% | — | LTO on/off to be measured |
| 13 | capi-network-http | `%lto_uncompatible_pkgs` | 0/2, 25 | 0/2, 24 | -4.0% | — | LTO on/off to be measured |
| 14 | capi-pc-ipc-proxy-tv | `%lto_armrel32_pkgs` | 0/1, 4 | 0/1, 7 | +75.0% | — | LTO on/off to be measured |
| 15 | capi-smsource | `%lto_armrel32_pkgs` | 0/3, 43 | 0/3, 35 | -18.6% | — | LTO on/off to be measured |
| 16 | capi-ui-autofill | `%lto_uncompatible_pkgs` | 0/5, 466 | 0/5, 356 | -23.6% | — | LTO on/off to be measured |
| 17 | com.samsung.tv.mvpd-native | `%lto_armrel32_pkgs` | 0/2, 175 | 0/2, 119 | -32.0% | — | LTO on/off to be measured |
| 18 | comss-api | `%lto_armrel32_pkgs` | 0/3, 21 | 0/3, 17 | -19.0% | — | LTO on/off to be measured |
| 19 | content-db | `%lto_armrel32_pkgs` | 0/2, 138 | 0/2, 94 | -31.9% | — | LTO on/off to be measured |
| 20 | content-service-framework | `%lto_armrel32_pkgs` | 0/11, 1,325 | 0/11, 1,148 | -13.4% | — | LTO on/off to be measured |
| 21 | context-aware-common | `%lto_armrel32_pkgs` | 0/1, 25 | 0/1, 16 | -36.0% | — | LTO on/off to be measured |
| 22 | data-provider-master | `%lto_uncompatible_pkgs` | 0/2, 875 | 0/2, 711 | -18.7% | — | LTO on/off to be measured |
| 23 | data-service-api | `%lto_uncompatible_pkgs` | 0/2, 50 | 0/2, 44 | -12.0% | — | LTO on/off to be measured |
| 24 | esg-api | `%lto_armrel32_pkgs` | 0/2, 193 | 0/2, 331 | +71.5% | — | Larger in LLVM; analysis first |
| 25 | fkp | `%lto_armrel32_pkgs` | 0/6, 1,271 | 0/6, 990 | -22.1% | — | LTO on/off to be measured |
| 26 | glslang | `%lto_armrel32_pkgs, %lto_pkgs` | 0/10, 3,686 | 0/10, 2,837 | -23.0% | — | LTO on/off to be measured |
| 27 | gst-plugins-atsc3 | `%lto_armrel32_pkgs` | 0/20, 1,093 | 0/20, 1,110 | +1.6% | — | LTO on/off to be measured |
| 28 | gstreamer-atsc3-pvr-plugins | `%lto_uncompatible_pkgs` | 0/5, 145 | 0/5, 124 | -14.5% | — | LTO on/off to be measured |
| 29 | hdcp | `%lto_armrel32_pkgs` | 0/12, 140 | 0/12, 119 | -15.0% | — | LTO on/off to be measured |
| 30 | ifw-thing | `%lto_armrel32_pkgs` | 0/3, 71 | 0/3, 66 | -7.0% | — | LTO on/off to be measured |
| 31 | iotivity | `%lto_uncompatible_pkgs` | 0/20, 2,133 | 0/20, 1,857 | -12.9% | — | LTO on/off to be measured |
| 32 | isf | `%lto_uncompatible_pkgs` | 0/16, 1,180 | 0/16, 786 | -33.4% | — | LTO on/off to be measured |
| 33 | lib-airplay-pal-tv | `%lto_armrel32_pkgs` | 0/6, 205 | 0/6, 158 | -22.9% | — | LTO on/off to be measured |
| 34 | libave | `%lto_armrel32_pkgs` | 0/8, 2,778 | 0/8, 2,372 | -14.6% | — | LTO on/off to be measured |
| 35 | libscreen_connector | `%lto_uncompatible_pkgs` | 0/10, 116 | 0/10, 75 | -35.3% | — | LTO on/off to be measured |
| 36 | libslive-dbus-proxy | `%lto_uncompatible_pkgs` | 0/1, 10 | 0/1, 9 | -10.0% | — | LTO on/off to be measured |
| 37 | libslive-dbus-stub | `%lto_armrel32_pkgs` | 0/2, 23 | 0/2, 21 | -8.7% | — | LTO on/off to be measured |
| 38 | libslive-provider | `%lto_uncompatible_pkgs` | 0/4, 659 | 0/4, 1,014 | +53.9% | — | Larger in LLVM; analysis first |
| 39 | libtar | `%lto_uncompatible_pkgs` | 0/2, 15 | 0/2, 13 | -13.3% | — | LTO on/off to be measured |
| 40 | libtizen_light-debugmenu | `%lto_armrel32_pkgs` | 0/2, 5 | 0/2, 5 | +0.0% | — | LTO on/off to be measured |
| 41 | libtvs-core | `%lto_armrel32_pkgs` | 0/10, 464 | 0/10, 396 | -14.7% | — | LTO on/off to be measured |
| 42 | libwidget_service | `%lto_uncompatible_pkgs` | 0/6, 622 | 0/6, 476 | -23.5% | — | LTO on/off to be measured |
| 43 | libwidget_viewer | `%lto_uncompatible_pkgs` | 0/10, 393 | 0/10, 298 | -24.2% | — | LTO on/off to be measured |
| 44 | logger | `%lto_uncompatible_pkgs` | 0/2, 43 | 0/2, 32 | -25.6% | — | LTO on/off to be measured |
| 45 | lynk | `%lto_armrel32_pkgs` | 0/5, 226 | 0/5, 192 | -15.0% | — | LTO on/off to be measured |
| 46 | mused | `%lto_armrel32_pkgs` | 0/4, 65 | 0/4, 56 | -13.8% | — | LTO on/off to be measured |
| 47 | org.tizen.applist | `%lto_uncompatible_pkgs` | 0/3, 5 | 0/3, 4 | -20.0% | — | LTO on/off to be measured |
| 48 | org.tizen.contents-recognition-service | `%lto_armrel32_pkgs` | 0/4, 2,934 | 0/4, 2,526 | -13.9% | — | LTO on/off to be measured |
| 49 | org.tizen.easysetup-daemon | `%lto_armrel32_pkgs` | 0/4, 1,857 | 0/4, 1,735 | -6.6% | — | LTO on/off to be measured |
| 50 | org.tizen.provider-setup | `%lto_armrel32_pkgs` | 0/3, 88 | 0/3, 64 | -27.3% | — | LTO on/off to be measured |
| 51 | org.tizen.RunningApps | `%lto_uncompatible_pkgs` | 0/3, 311 | 0/3, 220 | -29.3% | — | LTO on/off to be measured |
| 52 | org.tizen.ScreenMirroring-app-tv | `%lto_armrel32_pkgs` | 0/1, 8 | 0/1, 7 | -12.5% | — | LTO on/off to be measured |
| 53 | org.tizen.sealayer | `%lto_armrel32_pkgs, %lto_pkgs` | 0/2, 294 | 0/2, 221 | -24.8% | — | LTO on/off to be measured |
| 54 | org.tizen.sso-api | `%lto_armrel32_pkgs` | 0/3, 225 | 0/3, 177 | -21.3% | — | LTO on/off to be measured |
| 55 | org.tizen.ssoservice | `%lto_armrel32_pkgs` | 0/2, 2,724 | 0/2, 2,797 | +2.7% | — | LTO on/off to be measured |
| 56 | org.tizen.stand-by-scan | `%lto_armrel32_pkgs` | 0/3, 84 | 0/3, 281 | +234.5% | — | Larger in LLVM; analysis first |
| 57 | org.tizen.webappservice-api | `%lto_armrel32_pkgs` | 0/7, 562 | 0/7, 639 | +13.7% | — | LTO on/off to be measured |
| 58 | pulseaudio | `%lto_uncompatible_pkgs` | 0/79, 1,469 | 0/79, 1,358 | -7.6% | — | LTO on/off to be measured |
| 59 | pvod-appfw | `%lto_armrel32_pkgs` | 0/1, 17 | 0/1, 13 | -23.5% | — | LTO on/off to be measured |
| 60 | rpc-port | `%lto_uncompatible_pkgs` | 0/5, 979 | 0/5, 665 | -32.1% | — | LTO on/off to be measured |
| 61 | sdp | `%lto_uncompatible_pkgs` | 0/4, 252 | 0/4, 202 | -19.8% | — | LTO on/off to be measured |
| 62 | securestorage | `%lto_uncompatible_pkgs` | 0/29, 2,372 | 0/29, 1,851 | -22.0% | — | LTO on/off to be measured |
| 63 | settings-datafw | `%lto_armrel32_pkgs` | 0/4, 863 | 0/4, 813 | -5.8% | — | LTO on/off to be measured |
| 64 | smart-deadlock | `%lto_uncompatible_pkgs` | 0/7, 20 | 0/7, 18 | -10.0% | — | LTO on/off to be measured |
| 65 | smartsecurity2 | `%lto_armrel32_pkgs` | 0/8, 380 | 0/8, 315 | -17.1% | — | LTO on/off to be measured |
| 66 | spirv-tools | `%lto_armrel32_pkgs` | 0/10, 7,212 | 0/10, 4,742 | -34.2% | — | LTO on/off to be measured |
| 67 | storaged | `%lto_uncompatible_pkgs` | 0/6, 221 | 0/6, 168 | -24.0% | — | LTO on/off to be measured |
| 68 | tee_test_suite | `%lto_uncompatible_pkgs` | 0/34, 10,936 | 0/34, 10,444 | -4.5% | — | LTO on/off to be measured |
| 69 | tts | `%lto_armrel32_pkgs, %lto_uncompatible_pkgs` | 0/8, 769 | 0/8, 581 | -24.4% | — | LTO on/off to be measured |
| 70 | tvs-parser | `%lto_uncompatible_pkgs` | 0/2, 648 | 0/2, 529 | -18.4% | — | LTO on/off to be measured |
| 71 | tvs-si | `%lto_armrel32_pkgs` | 0/1, 300 | 0/1, 203 | -32.3% | — | LTO on/off to be measured |
| 72 | tvs-udm | `%lto_uncompatible_pkgs` | 0/1, 104 | 0/1, 71 | -31.7% | — | LTO on/off to be measured |
| 73 | tz-playservice | `%lto_uncompatible_pkgs` | 0/3, 59 | 0/3, 48 | -18.6% | — | LTO on/off to be measured |
| 74 | tz-spassservice | `%lto_uncompatible_pkgs` | 0/3, 52 | 0/3, 45 | -13.5% | — | LTO on/off to be measured |
| 75 | ug-rct | `%lto_uncompatible_pkgs` | 0/1, 19 | 0/1, 16 | -15.8% | — | LTO on/off to be measured |
| 76 | vd-net-config | `%lto_uncompatible_pkgs` | 0/6, 449 | 0/6, 392 | -12.7% | — | LTO on/off to be measured |
| 77 | vdsystem-lldb | `%lto_pkgs` | 0/4, 16,620 | 0/4, 12,215 | -26.5% | — | LTO on/off to be measured |
| 78 | voice-control | `%lto_armrel32_pkgs` | 0/10, 1,263 | 0/10, 970 | -23.2% | — | LTO on/off to be measured |
| 79 | webapi-contentsinfo-pepper-plugin | `%lto_uncompatible_pkgs` | 0/1, 29 | 0/1, 35 | +20.7% | — | LTO on/off to be measured |
| 80 | wifi-direct-manager | `%lto_armrel32_pkgs` | 0/3, 835 | 0/3, 636 | -23.8% | — | LTO on/off to be measured |
Not listed: 10 packages that are in an exclusion list but are LTO-linked in both images (avoc-daemon, capi-media-player, com.samsung.ep-plateau-agent, gstreamer-plugins-smsrc, gstreamer-plugins-tv, opencv, org.tizen.remote-management, org.tizen.tv-viewer, playready, qte-bm), and 38 listed packages not built for this product.

## 2. Bugs to fix: LTO lost in the LLVM image (not optimization)

These 18 packages were LTO-linked by GCC but have fewer LTO-linked ELF files in the LLVM image. They are migration bugs and are fixed separately.

| # | Package | List | GCC: LTO ELF / all | LLVM: LTO ELF / all | Cause / fix |
| --: | --- | --- | --- | --- | --- |
| 1 | ci-module | `%lto_uncompatible_pkgs` | 2/3 | 0/3 | In a Clang build.conf exclusion list but LTO-linked by GCC; review the exclusion |
| 2 | gst-ffmpeg-atsc3 | `%lto_pkgs` | 5/5 | 3/5 | In a Clang build.conf list but LTO-linked by GCC; review |
| 3 | ug-ics-efl | `%lto_uncompatible_pkgs` | 8/8 | 0/8 | In a Clang build.conf exclusion list but LTO-linked by GCC; review the exclusion |
| 4 | wpasupplicant | not in a list | 5/5 | 1/5 | Own link command without `-flto`; fixed by the r10 driver (LLVMgold passed to GNU ld by default); verify in next image |
| 5 | mm-omxil-impl-sec | not in a list | 39/39 | 15/15 | Same; verify in next image |
| 6 | wpasupplicant-license | not in a list | 4/4 | 0/4 | Same; verify in next image |
| 7 | systemd-boot-helper | not in a list | 11/11 | 10/10 | Same; verify in next image |
| 8 | libdbuspolicy | not in a list | 13/13 | 2/13 | Same; verify in next image |
| 9 | ext4-utils | not in a list | 3/3 | 0/3 | Same; verify in next image |
| 10 | linux-tizen-modules-source | not in a list | 4/4 | 0/4 | Same; verify in next image |
| 11 | freetype2 | not in a list | 1/1 | 0/1 | Same; verify in next image |
| 12 | soc-cpu-heavyload-ewtest | not in a list | 3/3 | 2/3 | Same; verify in next image |
| 13 | nsjail | not in a list | 2/3 | 0/3 | Same; verify in next image |
| 14 | libai-classifier-impl | not in a list | 3/3 | 2/3 | Same; verify in next image |
| 15 | libtbb | not in a list | 3/3 | 0/3 | Same; verify in next image |
| 16 | soc-ai-classifier | not in a list | 4/4 | 2/4 | Same; verify in next image |
| 17 | mic-bootstrap | not in a list | 591/1,611 | 565/1,799 | Build-host package, not installed on the TV |
| 18 | sys-tools | not in a list | 18/99 | 17/98 | Build-host package, not installed on the TV |
Source for both tables: ELF scan of the GCC image (Base 20260916.1, Product 20261001.3) and the LLVM image (Base 20261105.1, Product 20261112.1). LTO linkage is read from `.symtab` FILE symbols; `.text` from section headers.

## 3. Stability and ABI verification before enabling LTO (next plan)

No package in section 1 has been checked yet for API, ABI or runtime stability against the GCC build. That includes the four already enabled in build.conf@14452507. A package is removed from an exclusion list only after it passes all four checks below, so enabling LTO cannot change its interface or stability.

| # | Check | How | Pass criterion |
| --- | --- | --- | --- |
| 1 | Exported API vs GCC | Compare `.dynsym` exports, SONAME, `DT_NEEDED` and symbol versions of every shipped ELF: LLVM with LTO vs the GCC image | No removed or renamed export; no changed SONAME or symbol version; new exports only where explained |
| 2 | ABI vs GCC | `abidiff` on the debuginfo builds (GCC vs LLVM with LTO): function signatures, struct / class layout, enum values, vtables, TLS model; check exported inline and template functions that LTO may internalize | No ABI change reported, or each reported change reviewed and accepted by the package owner |
| 3 | Consumers | Link and load every package and TPK that depends on the library: `ldd` / loader check on the image and a start of each consumer | All consumers load; no unresolved symbols |
| 4 | Runtime stability | Smoke test of the package's main scenario, then a 24 h soak on KantSU2E with cores and crashes recorded; compare with the same scenario on the non-LTO build | No new core, crash or functional regression |

Order: first the four packages already enabled (on the matched rebuild next week), then the remaining candidates, largest `.text` first. Results go into the table below and into the size columns of section 1.

| # | Package | Exported API vs GCC | ABI vs GCC | Runtime stability | Status |
| ---: | --- | --- | --- | --- | --- |
| 1 | liballshare-core | Not tested | Not tested | Not tested | LTO already enabled in build.conf@14452507; check first on the matched rebuild |
| 2 | nagsam-mw | Not tested | Not tested | Not tested | LTO already enabled in build.conf@14452507; check first on the matched rebuild |
| 3 | org.tizen.tv.swu | Not tested | Not tested | Not tested | LTO already enabled in build.conf@14452507; check first on the matched rebuild |
| 4 | ug-hbbtv-efl | Not tested | Not tested | Not tested | LTO already enabled in build.conf@14452507; check first on the matched rebuild |
| 5 | acm-core | Not tested | Not tested | Not tested | Not tested |
| 6 | alsa-lib | Not tested | Not tested | Not tested | Not tested |
| 7 | antimalware | Not tested | Not tested | Not tested | Not tested |
| 8 | atsc3uhdcp | Not tested | Not tested | Not tested | Not tested |
| 9 | bixby-native-api | Not tested | Not tested | Not tested | Not tested |
| 10 | capi-appfw-app-context-manager | Not tested | Not tested | Not tested | Not tested |
| 11 | capi-billing-api-internal-tv | Not tested | Not tested | Not tested | Not tested |
| 12 | capi-billing-api-tv | Not tested | Not tested | Not tested | Not tested |
| 13 | capi-network-http | Not tested | Not tested | Not tested | Not tested |
| 14 | capi-pc-ipc-proxy-tv | Not tested | Not tested | Not tested | Not tested |
| 15 | capi-smsource | Not tested | Not tested | Not tested | Not tested |
| 16 | capi-ui-autofill | Not tested | Not tested | Not tested | Not tested |
| 17 | com.samsung.tv.mvpd-native | Not tested | Not tested | Not tested | Not tested |
| 18 | comss-api | Not tested | Not tested | Not tested | Not tested |
| 19 | content-db | Not tested | Not tested | Not tested | Not tested |
| 20 | content-service-framework | Not tested | Not tested | Not tested | Not tested |
| 21 | context-aware-common | Not tested | Not tested | Not tested | Not tested |
| 22 | data-provider-master | Not tested | Not tested | Not tested | Not tested |
| 23 | data-service-api | Not tested | Not tested | Not tested | Not tested |
| 24 | esg-api | Not tested | Not tested | Not tested | Not tested |
| 25 | fkp | Not tested | Not tested | Not tested | Not tested |
| 26 | glslang | Not tested | Not tested | Not tested | Not tested |
| 27 | gst-plugins-atsc3 | Not tested | Not tested | Not tested | Not tested |
| 28 | gstreamer-atsc3-pvr-plugins | Not tested | Not tested | Not tested | Not tested |
| 29 | hdcp | Not tested | Not tested | Not tested | Not tested |
| 30 | ifw-thing | Not tested | Not tested | Not tested | Not tested |
| 31 | iotivity | Not tested | Not tested | Not tested | Not tested |
| 32 | isf | Not tested | Not tested | Not tested | Not tested |
| 33 | lib-airplay-pal-tv | Not tested | Not tested | Not tested | Not tested |
| 34 | libave | Not tested | Not tested | Not tested | Not tested |
| 35 | libscreen_connector | Not tested | Not tested | Not tested | Not tested |
| 36 | libslive-dbus-proxy | Not tested | Not tested | Not tested | Not tested |
| 37 | libslive-dbus-stub | Not tested | Not tested | Not tested | Not tested |
| 38 | libslive-provider | Not tested | Not tested | Not tested | Not tested |
| 39 | libtar | Not tested | Not tested | Not tested | Not tested |
| 40 | libtizen_light-debugmenu | Not tested | Not tested | Not tested | Not tested |
| 41 | libtvs-core | Not tested | Not tested | Not tested | Not tested |
| 42 | libwidget_service | Not tested | Not tested | Not tested | Not tested |
| 43 | libwidget_viewer | Not tested | Not tested | Not tested | Not tested |
| 44 | logger | Not tested | Not tested | Not tested | Not tested |
| 45 | lynk | Not tested | Not tested | Not tested | Not tested |
| 46 | mused | Not tested | Not tested | Not tested | Not tested |
| 47 | org.tizen.applist | Not tested | Not tested | Not tested | Not tested |
| 48 | org.tizen.contents-recognition-service | Not tested | Not tested | Not tested | Not tested |
| 49 | org.tizen.easysetup-daemon | Not tested | Not tested | Not tested | Not tested |
| 50 | org.tizen.provider-setup | Not tested | Not tested | Not tested | Not tested |
| 51 | org.tizen.RunningApps | Not tested | Not tested | Not tested | Not tested |
| 52 | org.tizen.ScreenMirroring-app-tv | Not tested | Not tested | Not tested | Not tested |
| 53 | org.tizen.sealayer | Not tested | Not tested | Not tested | Not tested |
| 54 | org.tizen.sso-api | Not tested | Not tested | Not tested | Not tested |
| 55 | org.tizen.ssoservice | Not tested | Not tested | Not tested | Not tested |
| 56 | org.tizen.stand-by-scan | Not tested | Not tested | Not tested | Not tested |
| 57 | org.tizen.webappservice-api | Not tested | Not tested | Not tested | Not tested |
| 58 | pulseaudio | Not tested | Not tested | Not tested | Not tested |
| 59 | pvod-appfw | Not tested | Not tested | Not tested | Not tested |
| 60 | rpc-port | Not tested | Not tested | Not tested | Not tested |
| 61 | sdp | Not tested | Not tested | Not tested | Not tested |
| 62 | securestorage | Not tested | Not tested | Not tested | Not tested |
| 63 | settings-datafw | Not tested | Not tested | Not tested | Not tested |
| 64 | smart-deadlock | Not tested | Not tested | Not tested | Not tested |
| 65 | smartsecurity2 | Not tested | Not tested | Not tested | Not tested |
| 66 | spirv-tools | Not tested | Not tested | Not tested | Not tested |
| 67 | storaged | Not tested | Not tested | Not tested | Not tested |
| 68 | tee_test_suite | Not tested | Not tested | Not tested | Not tested |
| 69 | tts | Not tested | Not tested | Not tested | Not tested |
| 70 | tvs-parser | Not tested | Not tested | Not tested | Not tested |
| 71 | tvs-si | Not tested | Not tested | Not tested | Not tested |
| 72 | tvs-udm | Not tested | Not tested | Not tested | Not tested |
| 73 | tz-playservice | Not tested | Not tested | Not tested | Not tested |
| 74 | tz-spassservice | Not tested | Not tested | Not tested | Not tested |
| 75 | ug-rct | Not tested | Not tested | Not tested | Not tested |
| 76 | vd-net-config | Not tested | Not tested | Not tested | Not tested |
| 77 | vdsystem-lldb | Not tested | Not tested | Not tested | Not tested |
| 78 | voice-control | Not tested | Not tested | Not tested | Not tested |
| 79 | webapi-contentsinfo-pepper-plugin | Not tested | Not tested | Not tested | Not tested |
| 80 | wifi-direct-manager | Not tested | Not tested | Not tested | Not tested |