**Recorded project builds writing to `/home1/chengkai/p4fix_build`: none found. Planned steps requiring it: no. Historical use: documented.** The operator configs name it, and the old handover records a qb1111 root and per-package staging there. Two historical diagnostics searched it for iotivity logs and headers. Those reads and the surviving launch records do not establish who created its contents or whether staging contains the last copy of anything. **Deletion remains on hold until the operator reviews the native census and releases the directory.**

| Question | Evidence |
|---|---|
| Where did our measured builds write? | All 12 archived `GBS_START` launch lines across eight terminal transcripts specify `-B` under `vd-tree/workspace/temp`, covering nine distinct roots. These are the retained invocations, not an exhaustive command history. |
| What about the operator GBS config? | The preflight diff at lines 85–86 replaces the operator's `p4fix_build/gbs-root-qb37627297` with a private workspace root. A manual GBS invocation with an unmodified operator config could still use or recreate it. [Preflight transcript](../../artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt) |
| What was the historical dependency? | Maintained local memory `claude_mem/01_CLANG_MEMORY.md:390` identifies `gbs-root-qb1111` and `staging/oNNNN-<package>`. Local handover scripts `tizen-llvm-handover/hq-1114/backlog-probe.py:84` and `fix-input-bundle.py:53` search these paths as optional evidence sources. The retained iotivity warning log points to `workspace/temp/o1208`. Inspect staging before discarding unique inputs. |
| What about the running and planned jobs? | The kernel retry uses dkyJ0S, OwlD9Q, retained symbols, and new workspace lane roots. Package and Thumb builds rewrite the lane config or pass their private root via `-B`. Thumb QB preparation uses the retained workspace source/captures. The current workflow has no identified dependency on the legacy root. [Kernel matrix](../../artifacts/scripts/r0012f/kernel-matrix.py.txt) · [Package worker](../../artifacts/scripts/r0013a/pkg.py.txt) · [Thumb GBS launcher](../../artifacts/scripts/r0008a/gbs-thumb.py.txt) |

### Native census and dry-run

After the kernel diagnosis and package worker have been checked, run this in an idle maintenance window. The helper reads directory entries, allocated blocks, owner, newest descendant time, configs, process cwd/fds/maps and mount namespaces. It prints visibility gaps on an unprivileged run. A live sudo ticket enables full inspection. Expect minutes on a large home directory, one low-priority process and a small pinned GitHub download. The launcher verifies the script in memory.

```bash
p4audit() {
  local mode=dry
  case ${APPLY:-0} in 0) ;; 1) mode=apply ;; *) return 2 ;; esac
  /usr/bin/python3 -IB -c '
import hashlib, subprocess as sp, sys
url="https://raw.githubusercontent.com/lhmax2010/analysis/59d50f53e0eff34508446c2a14afe144481e37cc/artifacts/scripts/r0013h/p4fix.py.txt"
source=sp.check_output(["curl","-fsSL","--retry","4","--retry-all-errors","--connect-timeout","15","--max-time","120",url])
if hashlib.sha256(source).hexdigest()!="0d425481766a6be61b39a013b6fc0b6881c8796b5462cfc4618b77dcad24a501":
    sys.exit("HOLD script checksum")
priv=sp.run(["sudo","-n","true"],stdout=sp.DEVNULL,stderr=sp.DEVNULL).returncode==0
cmd=(["sudo","-n"] if priv else [])+["nice","-n","19","ionice","-c","3","/usr/bin/python3","-IB","-"]
sys.exit(sp.run(cmd+sys.argv[1:],input=source).returncode)
' "$mode" "$@"
}
APPLY=0 p4audit
```

Return the `ENTRY`, `PROCESS`, `MOUNT`, `CONFIG`, unreadable counts and token/hold lines. The output includes bytes and GiB for each top-level entry. Hard links inside the inventory are counted once. `ABSENT` closes the audit without further action. An active GBS or package/kernel worker defers the census. A full inspection needs the operator's live sudo ticket; after obtaining it, repeat the dry-run if the first pass reported incomplete visibility.

### Conditional removal

PM and the operator must first review the census, confirm that the visible staging contents and logs may be discarded, and reserve a window with no operator, OBS or GBS build starting. The script can detect running processes and hold the project locks; an independent manual build is outside those locks. Keep the same shell function from the dry-run. Use this separate command only after that review:

```bash
read -r -p 'Paste the reviewed 64-character DRY_RUN_TOKEN: ' p4audit_token
[[ $p4audit_token =~ ^[0-9a-f]{64}$ ]] && APPLY=1 p4audit "$p4audit_token"
```

The helper fixes the target to the canonical, non-symlink directory on the `/home1` device. It requires the reviewed inventory and config token, root visibility, no mount or live handle, and both existing project locks. It rechecks processes, mounts and directory identity immediately before the fd-safe removal. The free-space values are observations across the whole filesystem. No native census or deletion was executed from this checkout. [Helper for PM review](../../artifacts/scripts/r0013h/p4fix.py.txt)
