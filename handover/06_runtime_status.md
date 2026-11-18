# Runtime, ABI and stability

[Verified: user confirmation and target capture] A 10.0 LLVM product image has booted on KantSU2E. Current metadata collection saw 5,120 ARM ELF paths in the recorded scan scope. This neither proves the image is entirely Clang-built nor establishes complete functional acceptance.

## Passed scope

[Verified: retained crash report](../artifacts/historical-reports/usb-thumbnail-crash.md): the corrected Clang libavformat was mapped during USB-folder thumbnail generation and playback. User confirmed fast-forward/rewind, return to USB list and replay behaved normally. The source defect was uninitialized `pos_min`/`pos_max` passed into seek search, exposing undefined behavior under optimization. It was not a general GCC/Clang ABI incompatibility. Dual ARM package builds passed; GCC-build TV runtime and long-duration validation remain pending.

[Verified: scoped smoke](../artifacts/evidence/llvm101-smoke.txt): C compile/link/run, GCC/Clang C++ cross-DSO string and exception smoke, regular-LTO non-PIC fallback and explicit MLGO advisor code generation passed in a retained chroot/private ARM linker environment. These are not physical-TV stability results or production accelerator validation.

No complete TCT run, comprehensive application launch suite, repeated reboot acceptance or full long-term stability pass was recovered for the current image. Unknown test coverage must remain visible.

## Historical ABI cases for HQ

[Verified: shelf descriptions, translated with boundaries in the case table](../artifacts/shelf-cases.csv): five historical ABI/export/ODR case families are identified, but **only one is explicitly confirmed as a GCC-prebuilt calling-convention boundary case** in this reconciliation: bluetooth-host-impl / libbluetooth.so / CL14392070. Its `trivial_abi` mismatch caused register-versus-hidden-reference disagreement and SIGBUS; the recorded repair clears TRIVIAL_ABI at the boundary.

aul-1 and coba-source-native concern different internal class layouts and symbol binding across DSOs. key-manager concerns hidden template exports; cryptsetup concerns symbol versions. They must not all be reported as GCC-prebuilt defects. Symbol-version and latest-image runtime acceptance are distinct gates.

The case table also preserves alignment UB, incorrect inline-asm constraints, plugin lifetime, FORTIFY and missing-dependency cases. GCC strings or SIGBUS alone do not diagnose ABI incompatibility. Affected current-image package totals and before/after target performance are not established.

## Open behavior

[Verified: user observations retained in the current checkpoint] Playback brightness dimming recurred after temporary Motion Lighting intervention. The user deferred further diagnosis while building the next image. It remains open; no permanent fix is claimed.

[Verified: retained master plan] IoTivity `what()` lifetime/ABI work and residual SDK compatibility remain open. CL14452627 is the delivered compiler-selection shelf; a new lifetime candidate was not delivered. Critical media/HomeUI/HDMI/MAPI/SSO/ATSC3 regression and endurance need explicit current-image evidence.
