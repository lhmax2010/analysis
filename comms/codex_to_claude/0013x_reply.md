# 0013x · K4 Thumb-2 enumeration

```bash
(
set -eu
pin=3a1362f95adc86bc5d4119e97ba8181174d987e0
t=/home1/chengkai/vd-tree/workspace/temp
d=$(mktemp -d "$t/pm0013x-launcher.XXXXXX")
curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 180 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013x/enumerate.sh.txt" -o "$d/run.sh"
printf '%s  %s\n' 178e8bc3736f8bd4f6bb72712eb4f9663f6e9c7a488771646798e94fc7442c1a "$d/run.sh" | sha256sum -c -
bash "$d/run.sh" "$pin"
)
```

**Native server, attended terminal, after PM review.** The dependency lookup has a 50-second deadline. If admitted, allow roughly 1–4 hours for GBS and upstream source comparison. It uses six allowed CPUs, one package build, the existing queue and both heavy locks, and the existing 105 GiB free disk / 32 GiB available RAM admission. Writes go into a fresh `workspace/temp/pm0013n-enum.*` directory. The existing reclaim follower can continue using that naming scheme.

**DsfXAe result: `SETUP_FAILED deps`.** GBS reported `nothing provides secureboot-signer` and `nothing provides vd-kernel-dtb-devel`. The run created no ARM build root and never reached the compiler. It contributes zero observed assembler errors.

The launcher locates the K4 `GBS_START` in `pm0012-kernel.dkyJ0S/jobs/kernel-thumb/job.log`, matches its K4 output log and build root, and takes the config following **GBS's** `-c`. `ENUM_INPUT` prints the config path, SHA-256 and both literal repo URLs. `repo-provenance` stops the run if that trace cannot establish a unique config. The staging copy changes only the destination build root. The current armv7l primary metadata must identify an armv7l/noarch provider for both requirements before checkout or sudo.

DsfXAe's captured Product URL ends in `b776/19414776/…20261123.2/` and its empty local repo points to the original K4 directory. The surviving transcript establishes the dependency failure. Comparing the new `ENUM_INPUT` against that URL will distinguish a different repo from changed availability or earlier cached dependencies. An identical URL with unavailable providers still stops before GBS.

The native output distinguishes dependency failure, absent build root, and absent keep-going marker. The compiler report retains the original revision `fae92f998a51e8493e2ed452381aad73c2ce689e`, both make passes, macro notes and diagnostic context from the package and GBS logs. Return `ENUM_RESULT`, the JSON SHA-256 and the numbered `ENUM_PART` records. For a long packet, use the printed `READ_PART` command, changing its line number through the printed part count. A reachable-error inventory requires actual compilation. The assembly patch and touched-object A32 identity checks follow that inventory.

Python 3.10.12 fixtures reproduced the DsfXAe setup verdict, matched the K4 command to its config, exercised both provider outcomes and distinguished missing build root from missing make. The intranet provider result and enumerated sites await the native run.

## Archived originals

- [native-run-r0013n-enum-DsfXAe-20261127.txt](../../artifacts/evidence/native-run-r0013n-enum-DsfXAe-20261127.txt) · `2f03badb43703faeca9fc45aeec72c664931f0d45530daba20c264b36c7dee73`
- [native-run-r0013n-prebuild-DsfXAe-20261127.txt](../../artifacts/evidence/native-run-r0013n-prebuild-DsfXAe-20261127.txt) · `2cd7d1f1e4bf92c6e196bd049287a4b17d995362c51e24847021b7246dfea14b`
