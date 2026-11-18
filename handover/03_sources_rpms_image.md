# Sources, toolchain selection, RPMs and image

## Fixed inputs

[Verified: user-supplied configuration; current checkpoint]

```text
Config: /home1/chengkai/vd-tree/config/gbs_vd_llvm_11.16_qb37627297.conf
Quickbuild: 37627297
Base: http://repos.vd.sec.samsung.net/obs220/tizen-rsa/tizen-10.0-base-dev-llvm/standard/tizen-10.0-base-dev-llvm-standard_20261113.1/
Product: http://repos.vd.sec.samsung.net/priv/168.219.236.62:81/PRV/builds/b658/19350658/artifacts/TIZEN-ASAN-PUBLIC-KantSU2e-RELEASE_20261117.2/
Repository order: Product, then Base
Expected build.conf: migration/10.0/TV/TIZEN_KantSU2E_Clang_build.conf@14452507
Expected Base list: /home1/chengkai/vd-tree/manifest/tizen10.0_base_urls_1114_noprelink.txt
Expected shelf list: /home1/chengkai/vd-tree/manifest/tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt
```

[Verified: retained metadata ledger] Product has 5,880 available target RPM identities and Base 890, total 6,770. This is not the installed package count or number of source packages/builds. The plan records 2,245 unique Base paths and 930 ltoexp2 shelf paths. The previous 932-entry seek-only list remains a control. Full comments for the 930-entry list were received and reconciled; do not request them again.

[Verified: historical baseline report](../artifacts/historical-reports/hq-compiler-options-lto.md): GCC Base20260916.1 + Product20261001.3 is an older control; historical LLVM Product20261112.1 differs in source date. These are valid inventories with explicit scope, not a clean current GCC/LLVM causal comparison. Total RPM bytes for matched current compiler sets: unknown.

## Exactly how selection is expressed

[Verified: retained project-config diff](../artifacts/historical-reports/base-changes-part-05.md) records:

```text
%_toolchain %{?_toolchain_override}%{!?_toolchain_override:clang}
%__cc_clang %{_host}-clang
%__cxx_clang %{_host}-clang++
%__cc_gcc %{_host}-gcc
%__cxx_gcc %{_host}-g++
%__cc %{expand:%%{__cc_%{_toolchain}}}
%__cxx %{expand:%%{__cxx_%{_toolchain}}}
```

The same selection expands `%__ar`, `%__ranlib` and toolchain optflags. Historical defaults are Clang `-Os -fstack-protector` and GCC `-O2 -fno-inline-functions -fstack-protector-strong`, with shared platform flags. ARM platform optflags include `-mthumb`; later file/build-system overrides can win. These are retained configuration mechanisms, not proof of every current compile command.

[Verified: historical Base report] Project configuration preinstalls `clang-accel-<host>-<target>` alongside qemu acceleration, moves GCC/G++ from Required to Support, and supports Clang/llvm-devel. `%_toolchain_override` permits package exceptions. Specs must inherit the selected compiler and flags; SDK builds additionally require SDK-side selection. No evidence supports calling this a universal `update-alternatives` switch.

[Verified: historical report and candidate source] `gcc-contrib` restores `%{set_build_flags}` in `%__spec_build_pre` and calls `%{?clang_force_incompatible}`. `clang-contrib` supplies `clang-force-options` / `clang-unforce-options` and config hooks. The historical implementation was for public ASAN; equivalent regular-build force-options deployment remains a gate, not assumed done. `clang.cfg` also supplies platform compatibility defaults. Package-local CFLAGS/CXXFLAGS, configure probes and subbuilds must be audited at their final ordering.

## LLVM and runtime packages

[Verified](../artifacts/evidence/llvm101-bootstrap.txt): retained bootstrap uses LLVM 22.1.8 with projects `clang;lldb;clang-tools-extra;lld;compiler-rt;openmp`, target backends ARM/BPF in that build. LLVMgold belongs to llvm-devel; compiler-rt and libomp resource/runtime payloads were examined. LLD being packaged does not make it the production default linker.

[Verified](../artifacts/evidence/llvm101-smoke.txt): the VD driver passes LLVMgold to GNU ld by default subject to explicit disabling and link-mode guards. A link lacking `-flto` can still consume bitcode through that plugin: it is **not** sufficient evidence of a native path. The O4 compatibility patch maps to O3. The non-PIC fallback is regular-LTO IR code generation, not native machine-code rewriting.

[Verified: AVControl imports](../artifacts/evidence/avcontrol-size.txt) show GLIBCXX-versioned symbols. Preserve existing libstdc++/libgcc interoperability unless a separately reviewed runtime migration is authorized. No global libc++ switch was established. Cross-DSO string/exception smoke passed in both compiler directions, with limited coverage.

## Customized MLGO

[Verified: pinned source](../artifacts/evidence/mlgo-input-pin.txt): Gerrit `platform/upstream/llvm`, branch `sandbox/fangyu.he/custom_mlgo_model`, pinned commit `18307011adddd987a824ac53807ca91b8df1232a`. Source access supplied by user: `ssh://lhmax2025@review.tizen.org:29418/platform/upstream/llvm`. Minimal patch/assets were used to avoid a full history clone.

[Verified](../artifacts/evidence/mlgo-source-submit.txt): OBS `Tizen:10.0:Base:Dev:LLVM`, package `llvm`, revision 12, srcmd5 `0b38aead137ec42dcd99dee28091acc1`. It includes Custom inliner/regalloc plus all three SR runtime archives and normal-build input verification. The prior model-only revision 11 was incomplete and superseded. Independent macros select inliner, regalloc and runtime. Retain VD compiler/driver/PIC changes.

Latest captured ARM/x86 build states were `building`; no completed customized Base image or kernel performance result is established. Official/Custom comparison must hold the runtime constant, and separately prove actual LLVM advisor use.

## Image production

[Verified: user reports and board capture] A new LLVM product image was built/flashed/booted. Exact kickstart, image-generation invocation, image byte size, flash command and immutable board-to-QB mapping are **not recovered**. Do not infer them from a generic `latest` board release label. Quickbuild inputs are published Base list + build.conf + shelf list; source shelve acknowledgement is not a submitted Perforce change or image verification.

New seek shelf CL14466526 replaced the seek candidate for the next image; original CL14396810 was unchanged and workspace restored. Later ltoexp2 selection is the active experimental list. Full accepted-image provenance remains A0, including prelink policy and installed RPM identity.

[Verified, round 0002] The board reports Build ID `T-KSU2EJAKUC-0101-PERF-202611171009`. All 2,342 installed RPM identities matched fixed repository metadata by exact NEVRA with Product precedence. Confirm image-to-QB identity with a job export and correlate payloads by checksum and ELF Build ID. [Installed ledger](../artifacts/ledger/README.md)
