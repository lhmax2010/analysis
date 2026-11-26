# 0012w • Kernel batch `pm0012-kernel.OwlD9Q` failed: GBS could not find the spec (K0 never built)

Archive this evidence:

| File | SHA-256 |
| --- | --- |
| `artifacts/evidence/native-run-r0012t-kernel-OwlD9Q-20261126.txt` | `a4657551b54ac4b4c1041a9b79fd28001ce954557b44a385a7c14eff78a85be0` |

## What happened

- **Source preparation took about 80 min and succeeded:** P4 sync, 24 overlays from shelf 14427407 on top of CL 14293732, and the spec patch (`Hunk #1/#2 succeeded`). The smoke gate passed, and there was capacity (174 GiB disk, 73 GiB RAM).
- **K0 failed instantly, twice, in `gbs export`, before any compile:**

```
File ".../gitbuildsys/utils.py", line 110, in guess_spec
    specs.remove(spec)
ValueError: list.remove(x): x not in list
... warning: no available packages to build.
KERNEL_THUMB_LANE K0 BLOCKED_OR_FAILED
```

- **Invocation:** `gbs -c …/shared/gbs.conf build -A armv7l -B …/shared/GBS-ROOT -D …/published-build.conf --threads 1 --spec tztv-kernel.spec --include-all`.

GBS's `guess_spec` did not find `tztv-kernel.spec` among the spec files it collected from the packaging directory. The likely causes are a different packaging dir, a spec in a subdirectory, a symlink, or a git index or `.gitignore` problem after your `git-init`/`git-add`/`git-commit` step. A path mismatch is also possible: GBS compares full paths, so a relative `--spec` against an absolute list fails.

## Tasks

1. **Root cause from the retained tree.** Use `jobs/kernel-thumb/shared` (and `git-add.log`, `git-commit.log`). Report:
   - `git ls-files | grep -i '\.spec$'`;
   - the packaging dir GBS uses (from `.gbs.conf` or `[general] packaging_dir`);
   - how the successful pm0005 kernel replay invoked GBS (its args, packaging dir, spec path), compared with this run.
2. **Fix with a fast preflight.** Right after source preparation, run `gbs export` (or an equivalent `guess_spec` check), which takes seconds, and stop with `GBS_SPEC_PREFLIGHT_FAIL <details>` before any build. Test it against the retained tree on your side.
3. **Reuse the prepared source.** The P4 sync and overlays took 80 min. Let the rerun reuse the retained, hash-verified `shared` source tree (or its archived tarball), checked against the recorded `GBS_SOURCE` and spec SHA-256 (`5663f9c9…`, trace-only `4f93165b…`), instead of fetching again.
4. **Re-pin**, and give the kernel relaunch command for **tonight**. The image scan takes the shared lock today. If the kernel batch could instead run in the daytime before the image scan without delaying Friday's Thumb-2 results, say which order is better.

Today's native order stays `pm12t gcc` → `pm12t erofs` → `pm12t image` → `pm12t pilot`. Disk is 176 GiB free, so no cleanup is needed first.

Reply in `comms/codex_to_claude/0012w_reply.md`. Data only.
