# PM Handover Request: LLVM Adaptation & Performance/Memory Optimization on Tizen

Hi Codex. I'm Claude, and I'm taking over as PM for this task. Goal: **replace GCC with LLVM as the Tizen toolchain, then optimize performance and memory.** You keep doing the development, analysis and testing. I review your work, plan with you, and make decisions *together with you*.

I can't reach the Native Server or the local PC. I only see what you push to:
**https://github.com/lhmax2010/analysis.git** (empty right now)

This first round is **information gathering only**. Don't start new builds or heavy jobs. Only run light, read-only commands where you need to check a fact.

---

## 0. Ground rules (apply to every task from now on)

1. **Workspace only.** Every file you create on the local PC or the Native Server must stay inside the task workspace. Don't write outside it. If a tool needs a temp dir, point `TMPDIR` inside the workspace. Please tell me the exact workspace paths.
2. **GitHub is our only channel.** Everything I need goes into the repo. Push to `main` unless we agree on something else.
3. **Facts vs. assumptions.** Mark each important statement **[Verified]** (with the command, log path or file that proves it) or **[Assumption/Memory]**. If you don't know something, say so. Don't guess.
4. **No binaries in git.** Don't commit RPMs, images, build roots or anything over 20 MB. Give the path on the server, the size and the sha256 instead. Logs: commit summaries plus the relevant excerpts (error context, tails). Full logs only if small and compressed.
5. **Readable through the web.** I read the repo through GitHub's web pages, so keep the repo **public** until the task ends. Use `.md`, `.txt` or `.csv`, and split documents so no file is much over ~400 lines. Give every folder a README index with relative links.
6. **Passwords and tokens:** replace them with `<REDACTED>`. Hostnames, paths and IPs are fine.
7. **English** in all repo files.

## 1. Decision protocol (we review each other)

Create `decisions/DECISIONS.md`. Each decision gets an entry: ID, date, topic, options, **Codex position**, **Claude position**, final decision, status (`Proposed` / `Agreed` / `Escalated to user`).
- If you think any request or decision of mine is wrong, say so plainly and give your reasons. Don't just follow it. I'll do the same for your proposals.
- If we still disagree, we escalate to the user and don't proceed on that point.
- Also record the important decisions you **already made** before this handover (e.g. LLVM version, linker, C++ runtime, how clang is injected into the build), with your reasoning.

## 2. Repo layout to create

```
README.md                      # project overview + index of everything below
comms/
  claude_to_codex/             # I put my prompts here as files (NNNN_topic.md)
  codex_to_claude/             # your replies (NNNN_topic.md), same number as my request
decisions/DECISIONS.md
handover/                      # this round's deliverables (sections 3.1–3.10)
status/STATUS.md               # one-page current status, kept up to date every round
artifacts/                     # scripts, patches, small logs, CSVs (indexed)
```
Commit this prompt as `comms/claude_to_codex/0001_handover_request.md`.

---

## 3. Information I need (put each under `handover/`, one file per item)

### 3.1 `01_goal_and_scope.md`
- The goal as you understand it, and the **definition of done**: whole image built with LLVM? Which packages may stay on GCC (kernel, glibc, bootloader, Fortran/Go packages…)?
- Tizen version/profile (e.g. Tizen 10 / unified / headed/headless / TV / IoT), target arch(es) (armv7l / aarch64 / x86_64 / riscv64), and target device or emulator.
- Requirements and targets from the user or HQ (perf %, memory %, binary size, deadlines), and where they came from.
- Any relation to other projects (e.g. llvm-optimize, autofdo_bolt_agent): shared code, branches, patches or results.

### 3.2 `02_environment.md`
- **Local PC** and **Native Server**: hostname, OS, CPU cores, RAM, free disk, workspace paths, and which work runs where.
- How data moves between the Native Server, the local PC and GitHub.
- Usage limits: is the server shared? Are there time windows when heavy jobs are allowed? Max parallel jobs? Anything that must never happen (e.g. OOM or a reboot)?
- Tools and versions: gbs, mic, osc, qemu, sdb, the device/emulator, the LLVM/clang version(s), the GCC version currently used in Tizen.

### 3.3 `03_sources_rpms_image.md`
- Source location(s): git/Gerrit branches, snapshot/repo URLs and IDs, number of packages.
- Build config: `gbs.conf`, build.conf/prjconf, and the macros used. **Exactly how the toolchain is switched to LLVM**: spec changes, `%__cc`/`%__cxx` macros, cc wrappers, alternatives, the build-root package set.
- The toolchain packages themselves (llvm/clang/lld/compiler-rt/libc++ or libstdc++/libgcc specs) and where they're built.
- Image: kickstart file(s), how the image is created, image size, and how it's flashed or booted.
- RPM inventory: where the GCC-built and LLVM-built RPM sets are, counts, and the total size of each.

### 3.4 `04_work_done.md`
- What's done so far, organized by phase or milestone (not a day-by-day log), with dates.
- Patches made: count, which packages, where they're stored. Put a patch index (CSV: package, patch file, reason, upstreamable?) in `artifacts/`.
- Scripts and automation you built: what each does, and where it lives.

### 3.5 `05_build_status.md`
- GCC vs LLVM package build results: total / pass / fail / skipped. Commit the full per-package table as `artifacts/build_status.csv` (package, GCC result, LLVM result, failure category, fixed?, note).
- Failure categories with counts and one representative example each. For example: new `-Werror` warnings, GNU extensions (nested functions, VLAIS), inline asm, `-fno-common`/symbol issues, C++ runtime/ABI, linker (lld vs bfd/gold, version scripts), LTO, configure checks, missing `-m`/`-f` flags, and test-suite failures.

### 3.6 `06_runtime_status.md`
- Has the LLVM-built image been built, flashed and booted? Which test suites ran (smoke, TCT, app launch, others) and what were the results?
- Runtime crashes or behavior differences vs the GCC image, and their root causes if known.

### 3.7 `07_perf_memory.md`
- Benchmark and measurement method for each metric: boot time, app launch time, specific benchmarks, binary/RPM/image size, RSS/PSS/USS, page cache, free memory after boot. Include the tools, number of runs and variance.
- **GCC baseline vs LLVM** results so far. Commit the raw numbers as CSV in `artifacts/`.
- Optimizations tried or planned, with results: -O2/-Os/-Oz, ThinLTO/LTO, PGO/AutoFDO, BOLT, ICF, `--gc-sections`, `-fvisibility=hidden`, RELR/packed relocations, hash style, `-fno-plt`, machine tuning flags, etc.

### 3.8 `08_issues_risks.md`
- Open blockers, known bugs and risks (technical, schedule, environment), each with severity and your proposed way forward.

### 3.9 `09_proposed_plan.md`
- Your proposed next steps and priorities, with rough effort estimates and what each step needs (machine time, user/HQ input).
- Any open questions for me or the user.

### 3.10 `10_artifacts_index.md`
- Index of everything in `artifacts/`, plus important items that stay on the servers (path, size, sha256, what it is).

---

## 4. When you're done
1. Write `status/STATUS.md` (one page: where we are, top 3 issues, next step).
2. Write `comms/codex_to_claude/0001_handover_reply.md` with: a short summary, the list of files pushed, anything you couldn't collect and why, and any disagreement with these rules.
3. Push, then give the user the **commit hash** so they can pass it to me.

## 5. Addendum: overall progress (you own the master tracker)

The user says you are tracking the whole progress of this task. Please share it in full. Don't rebuild it from memory: export it from wherever you actually keep it (tracker file, notes, plan doc), and tell me where that source is.

Add `handover/00_overall_progress.md`, and make it the first file listed in README.md:

1. **Master plan:** every phase/milestone from the beginning through "GCC fully replaced + perf/memory optimized". For each item give: ID, description, owner, status (`Done` / `In progress` / `Blocked` / `Not started`), % complete, start and end dates (actual or planned), and evidence (link to the file or log in this repo).
2. **Overall completion estimate**, split into (a) LLVM adaptation (builds/boots/passes tests), (b) performance optimization, and (c) memory optimization. Explain how you calculated each %.
3. **Currently running work:** anything running on the Native Server or local PC right now (builds, tests, benchmarks). Give what it is, when it started, the expected finish time, and where its output will land.
4. **Last 2 weeks:** what was finished and what changed in the plan, with reasons.
5. **Pending from the user or HQ:** approvals, answers or resources you're waiting on.

Also commit the machine-readable version as `artifacts/progress_tracker.csv` (same columns as item 1).

From now on, update `status/STATUS.md` and the tracker in **every** round you push, so the repo always reflects the current state. I'll review progress only through these two files.