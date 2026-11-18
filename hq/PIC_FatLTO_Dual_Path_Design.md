# PIC validation for both FatLTO link paths

Thank you for the careful review. The earlier validation missed part of the native consumption path. We ran a paired Tizen ARM matrix and propose separate checks for both routes.

FatLTO objects carry IR for the matching LTO backend and an already generated native object for consumers that select it. In a regular LLVM LTO link, the plugin uses the bitcode and its PIC metadata. The existing fallback regenerates code for the requested shared or PIE output where its rules apply. Its warning covers the IR path. With a native link or cross-compiler consumption of the native portion, the relocation assumptions are fixed at compile time. The IR warning is unavailable on that path. Keep FatLTO available for mixed-toolchain builds and compile reusable native code with PIC where the consumers require it.

## Verified matrix

| Input and output | Expected check | Observed Tizen ARM result |
|---|---|---|
| GCC and Clang PIC objects/archives to shared and PIE | Matched LTO and explicit native paths link and run | Positive fixtures passed |
| GCC and Clang non-PIC objects/archives, including fat inputs, through their matching regular LTO route | Check code generation, relevant diagnostics and output runtime behavior | Tested LTO cases linked and ran |
| Same non-PIC inputs, through GCC/direct native paths for shared or PIE with strict text-relocation policy | Check explicit native route and relocation failure | 18 native cases rejected |
| Successfully linked fixtures | Check actual load/run and control behavior | 38 of 56 synthetic cases linked and passed, with 90 passing invocations |

These are synthetic fixtures and strict linker outcomes. Record producer, exact input hash, effective native or plugin path and final output type. In particular, invoking the driver without `-flto` alone cannot establish the native route because the driver may still claim bitcode. A separately compiled no-LTO RPM is a distinct case. If it builds all inputs consistently with PIC, fat-object reuse may be irrelevant. Verify any carried-in archives and prebuilt members independently.

## Producer and release policy

1. Apply targeted `-fPIC` to sources whose objects are shipped in development/static packages or consumed by a shared-library or PIE build. Verify final per-file options in every subbuild and both LTO/no-LTO variants. Keep intentional fixed-address, startup and firmware cases tied to their actual consumers.
2. Screen ARM32 relocatable ELF/archive members. In relocations targeting executable sections, flag ABS32, absolute ARM/Thumb MOVW/MOVT and TLS local-exec evidence. Record the member, target section, LLVM/GNU bitcode markers, producer evidence and any intended-use exception. Review context before declaring a defect. Some valid native consumers use absolute relocations. Absence of listed relocations leaves other link constraints to be checked. [Arm ELF relocation specification](https://github.com/ARM-software/abi-aa/blob/main/aaelf32/aaelf32.rst)
3. Validate the screen against all 56 retained inputs, requiring no flagged PIC fixtures and coverage of the 18 observed native rejects. The initial ARM assembler smoke found the expected code relocations and excluded the debug-only absolute relocation. Full retained-fixture validation is pending.
4. Screen the 92 pinned RPM identities with direct static paths, 43 Product and 49 Base. For each hit, identify the actual consumer and its link flags. Keep build-tree-only inputs such as internal gst-ffmpeg static dependencies, suffixless inputs and nested containers in a separate census. The nine previously identified consumer acceptance entries remain the first targeted replay batch. Production affected-package count and measured size, performance and stability deltas are pending.
5. Design an advisory post-build check using the same classification and packaging metadata. Begin with a report of unqualified inputs and narrowly documented exceptions. Move a consumer to enforcement only when its producer policy and positive/negative controls are verified.

For pure-native GCC/vendor inputs, obtain or build a PIC variant or reject the incompatible consumer. Arbitrary native instruction rewriting is outside the design. Keep ordinary runtime ABI review separate, including the documented prebuilt Bluetooth shared-interface mismatch. If wider PIC policy is proposed, compare paired ARM32 builds for code size, relocations, startup, media throughput and memory on matched hardware before adoption.
