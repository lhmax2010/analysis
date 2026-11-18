# Proposed KantSU2E measurement protocol

[Assumption/Memory: D-013 proposal] Freeze physical board identity, image Build ID, checksum and source inputs, firmware/MICOM, update policy, display mode, attached peripherals, network, ambient/board temperature and software workload. Hold these constant within blocked alternated control and candidate runs. Record actual start/end, run ID, scenario, versioned media inputs and raw logs. Predefine valid-run criteria.

| Scenario | Definition | Repetitions | Metrics |
|---|---|---:|---|
| Cold boot | Standard powered-off interval to one verified Home-ready log milestone | 10 | Elapsed monotonic time and boot failures |
| App launch | Launch from Home to first stable interactive frame, separately in cold/warm states | 10 per app/state | Latency, crashes and launch failures |
| Settled idle | Home with fixed settings and no foreground tasks 10 minutes after boot | 5 boots | PSS sum, top 20 PSS/USS, Slab, Cached, MemAvailable |
| Media playback | Use fixed samples, local USB, then fixed local network source on HomeUI player | 10 paired runs proposed | Late/dropped frames, stalls, minimum available memory, major faults/refaults, LMK/OOM, zram deltas and media-process PSS/USS |
| 4K at physical 1 GB budget | Same board and stream under verified D-020 conditions | 3 each for A/B method comparison; candidate repetitions after variance pilot | Same media measures plus playback continuity |
| Size | Exact matching image/package scope and compression settings | One artifact pair plus repeatability check | Image and RPM installed bytes, ELF PT_LOAD file and memory sizes |

Proposed five applications are Home UI, Settings, Source/USB browser, built-in media player and TV channel viewer. Fix the entry action, initial page and terminal event on the actual target before the first scored run. Home-to-Home and boot timing are separate measurements. A local known seek sample is the functional regression control. Use a fixed 4K HEVC Main 10 MP4 clip, preferably 2160p60, and a versioned equivalent local HLS source for streaming pressure. Select real samples, record bitrate, stream protocol, hashes and playback counters before scoring. Start with supported hardware-decode settings and fixed audio/video output.

Retain individual observations. Report median, IQR and a 95% interval for the paired change. Initial relative regression threshold is 2% with an interval excluding zero. Wide intervals that still permit material regressions remain inconclusive. For stalls, LMK/OOM and other rare or zero-valued events define absolute tolerances and use an explicit correctness gate. Adopt only where an improvement is measured in at least one scenario and the others meet the agreed margins.

## GCC control

[Verified] The historical GCC Base/Product snapshots differ from the current LLVM source set. A flashable identical-source GCC KantSU2E image is unverified. The recorded GCC config references another Product and a mutable Base URL. A package-level `%_toolchain_override gcc` confirms a selection mechanism, while a GCC whole-image control requires source/shelf and repository freeze, validation of exceptions and SDK/runtime routes, and reproducible QB plus device qualification. Initial estimate is one engineer day to reconcile manifests and queue a controlled build, then actual QB elapsed time plus a boot/smoke slot. A formal manifest change requires a decision under D-018. [Source and image notes](03_sources_rpms_image.md)

Optimization candidates use Clang-to-Clang controls with identical sources and one changed flag or package policy. Use the full target protocol only after small pilot variance and counter checks.

Round 0003 adds an absolute gate for any new crash, LMK/OOM kill, ANR or audio/video underrun signature. Record free/min watermarks for each memory zone during playback. D-021 uses a shorter weekly comparison with the same controls. Keep those samples labelled.
