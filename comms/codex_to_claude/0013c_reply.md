```bash
(
  set -eu
  cd /home1/chengkai/vd-tree/workspace/temp
  d=$(mktemp -d "$PWD/pm0013-get.XXXXXX")
  pin=f866b36094805a433eac275d87ec88e4c2059212
  curl -fsSL --retry 4 --retry-all-errors --connect-timeout 15 --max-time 150 "https://raw.githubusercontent.com/lhmax2010/analysis/$pin/artifacts/scripts/r0013a/run.sh.txt" -o "$d/run"
  printf '%s  %s\n' 61039100608c06fcb7bcf61b205983937f48bc43c8f8d8bdad98674d348869c4 "$d/run" | sha256sum -c -
  bash "$d/run" "$pin" b5a28fd509920a9876cbfe46f66bb734e2e551fe82f1e092af9daa38f6f5c56f pkg
)
```

**Command 2 only.** Run from a separate foreground terminal or attached screen on the native host after refreshing the P4 ticket. The launcher prints the remaining ticket lifetime and prompts for sudo once. GBS shares that controlling terminal. The keepalive refreshes the sudo ticket every 45 seconds and the launcher stops the keepalive on exit.

| Event | Result |
|---|---|
| P4 status fails at startup or before Product source staging | `PKG_STOP p4-ticket`. A ticket that expires during a failed staging operation is also rechecked. |
| Noninteractive sudo fails before the worker, a package or an admitted lane | `PKG_STOP sudo`. Completed package receipts are retained. |
| Lane has at least 74 GiB disk, less than 28 GiB available RAM | `PKG_WAIT ram`. Recheck at five-minute intervals, bounded by Friday 09:30 CST. |
| Free disk below 74 GiB at admission | Stop. The existing 60 GiB floor also applies during the worker's GBS process. |

One low-priority package worker, six eligible cores, one GBS thread, nice 19, idle I/O, dedicated `pm0013-pkg.lock` and private roots. Network traffic depends on the downloaded RPMs and sources. Runtime is bounded by the Friday cutoff for admitted builds and RAM waits. The previously approved commands 1 and 3 use their existing `9047570` pin and gates.

**Local validation.** Python 3.10.12 under a controlling pseudo-terminal exercised the actual `run_owned`. The child and parent shared session 6 and foreground group 6. The GBS stand-in used process group 7, opened `/dev/tty`, and its descendant received SIGTERM through `killpg` when the worker stopped. Simulated lane admission waited 300 seconds on the test clock at 1 GiB available, admitted at 28 GiB, and stopped immediately at 73 GiB free disk. Credential-failure fixtures produced the two distinct stop reasons. All 25 indexed hashes matched at the script pin, and the launcher passed `bash -n`. Native sudo, P4 and build results await execution. [Fixture](../../artifacts/tests/r0013c/pkg_session.py)

**Index SHA-256** `b5a28fd509920a9876cbfe46f66bb734e2e551fe82f1e092af9daa38f6f5c56f`. One entry changed, the package worker, now `f16aa4eb547533b6960c16f088f0a283b79a7ce916736c1cf42b40c5ffd3a202`.

### Script diff against 9047570

```diff
diff --git a/artifacts/scripts/r0013a/pkg.py.txt b/artifacts/scripts/r0013a/pkg.py.txt
index 76b00e9..7257cc9 100644
--- a/artifacts/scripts/r0013a/pkg.py.txt
+++ b/artifacts/scripts/r0013a/pkg.py.txt
@@ -26,10 +26,33 @@ class Stop(Exception):pass
 def capacity():
     if time.time()>=CUTOFF:raise Stop("Friday 09:30 CST cutoff")
     if shutil.disk_usage(HERE).free<60*1024**3:raise Stop("60 GiB free-space floor")
+def check_credential(command, reason):
+    try:
+        result = subprocess.run(command, capture_output=True, text=True, errors="replace")
+    except OSError as exc:
+        raise Stop(reason) from exc
+    if result.returncode:
+        raise Stop(reason)
+
+def admit_lane(work, reserve_disk, reserve_ram):
+    while True:
+        free = shutil.disk_usage(work).free // 1024**3
+        info = Path("/proc/meminfo").read_text()
+        ram = int(re.search(r"(?m)^MemAvailable:\s+(\d+)", info)[1]) // 1024**2
+        print(f"PKG_ADMISSION free={free}GiB mem_available={ram}GiB lane={work.name}", flush=True)
+        capacity()
+        if free < 50 + reserve_disk:
+            raise Stop(f"disk admission requires {50 + reserve_disk} GiB")
+        if ram >= 16 + reserve_ram:
+            check_credential(["sudo", "-n", "true"], "sudo")
+            return
+        print("PKG_WAIT ram", flush=True)
+        time.sleep(max(0, min(300, CUTOFF - time.time())))
+
 def run_owned(cmd,cwd,log,timeout,check=True):
     capacity()
     with log.open("wb") as out:
-        with subprocess.Popen(cmd,cwd=cwd,stdout=out,stderr=subprocess.STDOUT,start_new_session=True) as p:
+        with subprocess.Popen(cmd,cwd=cwd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=os.setpgrp) as p:
             end=time.time()+timeout
             try:
                 while p.poll() is None:
@@ -141,7 +164,7 @@ def worker():
         if not root.resolve().is_relative_to(HERE) or root.exists():raise ValueError("root must be new and private")
         return re.sub(rb"(?m)^(\s*buildroot\s*=)[^\r\n]+",lambda m:m[1]+b" "+os.fsencode(root),data,count=1)
     if len(re.findall(rb"(?m)^\s*buildroot\s*=",template))!=1:raise ValueError("ambiguous GBS root in template")
-    gbs=SimpleNamespace(**lib("gbs-mlgo-t7"));gbs.execute=run_owned
+    gbs=SimpleNamespace(**lib("gbs-mlgo-t7"));gbs.execute=run_owned;gbs.available=admit_lane
     ole["configure_gbs"]=configure
     settings=SimpleNamespace(gbs=gbs,lib=repo,scan=scan,ole=ole,stager=lib("thumb-qb-sample"),thumb=lib("gbs-thumb"),
        inventories={k:[r for r in inv if r["repo"]==k] for k in ("Product","Base")},config=template,product=product,buildconf=buildconf)
@@ -159,6 +182,7 @@ def worker():
     print("PKG_PLAN",len(plan),"unranked",sorted(targets-set(sizes)),flush=True)
     for idx,(key,n) in enumerate(plan):
         capacity()
+        check_credential(["sudo", "-n", "true"], "sudo")
         work=HERE/(f"{idx:03d}-"+key+"-"+n);work.mkdir()
         result={"step":key,"package":n,"source_assumption":"Product P4 pin plus retained Nov16 shelf list; new submission list unproved"}
         try:
@@ -170,8 +194,13 @@ def worker():
                 archive=lib("matched-qb")["find_srpm"](repo,"official",work,sr)
                 src,spec=ole["stage_srpm"](sr,dict(path=str(archive),sha256=gbs.sha(archive)),work)
             else:
+                check_credential(["p4", "login", "-s"], "p4-ticket")
                 shelves=gbs.pinned(WS.parent/"manifest/tizen10.0_shelves_1116_ffmpeg_seek_ltoexp2.txt",ole["SHELVES"])
-                src,spec=ole["source_for"](gbs,repo,settings.stager,row,candidates,shelves,{},work)
+                try:
+                    src,spec=ole["source_for"](gbs,repo,settings.stager,row,candidates,shelves,{},work)
+                except (OSError, ValueError, subprocess.SubprocessError):
+                    check_credential(["p4", "login", "-s"], "p4-ticket")
+                    raise
             original=spec.read_text();spec.chmod(spec.stat().st_mode|0o200)
             gbs.local_git(src,work)
             recipe=rs[key] if key in rs else dev["base_recipe"](key)
@@ -201,4 +230,7 @@ if __name__=="__main__":
     with (WS/"temp/pm0013-pkg.lock").open("a") as lock:
         fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
         try:capacity();worker()
-        except Stop as reason:print("PKG_STOP",reason,flush=True)
+        except Stop as reason:
+            print("PKG_STOP", reason, flush=True)
+            if str(reason) != "Friday 09:30 CST cutoff":
+                sys.exit(2)
diff --git a/artifacts/scripts/r0013a/run.sh.txt b/artifacts/scripts/r0013a/run.sh.txt
index 45eeb3d..d9b23c1 100644
--- a/artifacts/scripts/r0013a/run.sh.txt
+++ b/artifacts/scripts/r0013a/run.sh.txt
@@ -43,7 +43,18 @@ bce)
     cat E.status
     if [[ -e E.log ]]; then tail -16 E.log | cut -c1-1800; fi ;;
 pkg)
+    [[ -t 0 ]] || { echo "PKG_STOP terminal"; exit 2; }
+    if ! ticket=$(p4 login -s 2>&1); then
+        printf 'PKG_STOP p4-ticket %.350s\n' "${ticket//$'\n'/ }"
+        exit 2
+    fi
+    printf 'P4_TICKET %.350s\n' "${ticket//$'\n'/ }"
+    sudo -v || { echo "PKG_STOP sudo"; exit 2; }
+    (while sleep 45; do sudo -n -v || exit 1; done) &
+    keeper=$!
+    trap 'kill "$keeper" 2>/dev/null || :; wait "$keeper" 2>/dev/null || :' EXIT
     stage pkg
+    sudo -n true || { echo "PKG_STOP sudo"; exit 2; }
     job pkg python3 -Bu pkg.py.txt
     cat pkg.status; tail -35 pkg.log | cut -c1-1800 ;;
 roster)
```
