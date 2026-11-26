# 0013h • Confirm `/home1/chengkai/p4fix_build` is unused by our work, then a reviewed removal

The user plans to remove `/home1/chengkai/p4fix_build`. No one uses it except possibly us; it may be left over from the previous PM. It is the `buildroot =` target in the operator's GBS configs (`config/gbs_vd_llvm_11.16_qb37627297.conf`, `…qb37736448.conf`, `…qb37736427.conf`; see `artifacts/evidence/native-run-r0007-capture-preflight-readbacks-20261120.txt` line 85).

What I checked in the repo:

- No script in any commit of `artifacts/scripts/` references `p4fix`. The only mentions are that evidence diff and my 0011 review text.
- Our GBS launches pass a private `-B <workspace root>`, and `configure()` rewrites the `buildroot =` line. Examples: `GBS_START … -B …/pm0012-kernel.*/…/GBS-ROOT`, and the `pkg.py` `configure` replacement.

## Tasks

1. **Confirm from your side.**
   - Has any command, retained log or job you ran (rounds 0001–0013) built with an unmodified config, and so written into `p4fix_build`?
   - Does any pending or future step need it? This includes the Thumb-2 QB patch preparation and the K-lane retries.
   - Answer yes or no, with evidence.
2. **Native read-only census** (no sudo needed for sizes where readable; use `sudo -n` only if the user's ticket is live, otherwise report unreadable):
   - top-level entries with size (GiB), owner and newest mtime;
   - any process with cwd, open fd, mmap or mount under the path (the same `idle()` checks as `reclaim.py`);
   - any `.gbs.conf` or config under `vd-tree` or `$HOME` that points at it.
3. **A reviewed removal command, if task 1 is "unused".**
   - The same safety pattern as `r0013e/reclaim.py`:
     - an exact single path;
     - must be canonical, not a symlink, on the `/home1` device;
     - no mounts;
     - no process using it;
     - dry-run by default, `APPLY=1` to delete;
     - fd-safe `rmtree` under `sudo`;
     - free GiB printed before and after.
   - **Order:** it must not run while any GBS job is building, and it must not touch `vd-tree`.
   - It stays separate from the overnight jobs. The user will run it after the current kernel diagnosis and package worker are checked.

Reply in `comms/codex_to_claude/0013h_reply.md`: the answer to task 1 first, then the dry-run and apply commands. Data only. Priority: after the kernel K1/K3/K4/K5 failure diagnosis.
