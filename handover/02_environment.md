# Environments and transfer workflow

[Verified: current local read-only capture](../artifacts/evidence/local-environment.txt): local hostname `toolchain-2026`, Ubuntu 24.04.5 LTS, x86_64, 20 logical CPUs, approximately 30.8 GiB RAM. Exact available memory and disk bytes are in the timestamped capture and change over time. The workspace had approximately 83 GiB free at export.

| Location | Workspace / role | Knowledge boundary |
|---|---|---|
| Local PC | `/home/toolchain/Desktop/temp`; review repo `/home/toolchain/Desktop/temp/analysis` | [Verified] current environment |
| Maintained memory | `/home/toolchain/Desktop/temp/claude_mem` | [Verified] source reports, index and log |
| Native server | `/home1/chengkai/vd-tree`; experiments in `workspace/temp` | [Verified] user-returned command paths |
| Native hostname | `risc-v-Alienware-Aurora-R16`, user `chengkai` | [Verified] returned terminal prompts; not an OS/CPU probe |
| TV | `192.168.108.13:26101`, KantSU2E; additions confined to `/root` | [Verified] retained SDB capture; earlier .25 address was corrected |
| GitHub | `lhmax2010/analysis`, `main`, public | [Verified] repository metadata this round |

Native server OS, cores, RAM, currently free disk and exact shared-user load: **unknown in reviewed current evidence**. Hardware name is not a resource measurement. Sharing policy, heavy-job windows and maximum global concurrency are not established. The retained isolated LLVM bootstrap used six compile jobs and two link jobs; that is not a general server capacity approval.

## Tool versions

| Tool | Local PC | Native / retained build environment |
|---|---|---|
| gbs | [Verified] `gbs --version`: 2.1.1 | Not independently recaptured |
| osc | [Verified] `osc --version`: 0.183 | Not independently recaptured |
| sdb | [Verified] `/home/toolchain/.local/bin/sdb version`: 4.2.36 | PC is the target connection endpoint |
| Git | [Verified] `git --version`: 2.43.0 | Not independently recaptured |
| mic | Not on PATH in this check | Unknown |
| qemu | `qemu-arm` not on PATH in this check | [Verified] retained provider identities in RPM layout evidence; exact executing binary version not rechecked |
| Clang | Current PC compiler not relevant to reported target builds | [Verified] 22.1.8 in retained 10.0/10.1 evidence |
| GCC | Current PC compiler not used for target acceptance | [Verified] Tizen GCC 14.2.0 in retained configuration |

[Verified](../artifacts/evidence/llvm101-rpm-layout.txt): the retained 10.1 acceleration package set includes `qemu-accel-x86_64-armv7l`, `qemu-linux-user-x86_64-cross` and binutils. The observed accelerated ld is x86_64 while the new LLVMgold RPM payload is ARM32. Exact executable architecture matters more than the name of the containing armv7l RPM.

## Workflow and constraints

[Verified: user instructions and archived exchanges] Codex supplies embedded Python/shell commands. The user runs intranet operations and returns reports/attachments. Base/Product repository access is intranet-only from this PC; no direct native-server SSH route has been provided. User-returned reports are preserved with hashes and decoded/checked locally. The TV has been reachable over SDB, separately from intranet package access.

GitHub plugin authentication has read-only permission on this repository. Existing local SSH authenticated as `lhmax2010`; publication uses that Git transport. No credentials are copied into the repository. This is a transport fallback, not a change to repository permissions.

Use `TMPDIR=/home/toolchain/Desktop/temp/analysis-work/tmp` locally and disable Python bytecode with `-B`. Build caches/output must remain in the authorized workspace. The supplied GBS configuration contains an old buildroot outside `vd-tree`; new execution must override it into `vd-tree`.

No server reboot, global compiler replacement, binfmt change, broad cleanup or target package installation is authorized by this information-only handover. Retain builds and evidence. Resource-heavy work should be scheduled after capacity confirmation; avoid concurrent large LLVM builds by assumption.
