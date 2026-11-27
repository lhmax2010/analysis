"""Exercise the native download layout, an expiring Product and an offline S12 replay."""
from contextlib import redirect_stdout
import gzip
import hashlib
import io
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
from unittest.mock import patch
from urllib.error import HTTPError

scripts=Path(__file__).resolve().parents[2]
repo=scripts.parents[1]
def sha(data):
    return hashlib.sha256(data).hexdigest()

with tempfile.TemporaryDirectory() as tmp:
    stage=Path(tmp)
    for launcher in ("r0013x/enumerate.sh.txt","r0013y/read.sh.txt"):
        path=scripts/launcher
        subprocess.run(["bash","-n",path],check=True)
        for line in path.read_text().split("done <<'PINS'\n")[1].split("\nPINS")[0].splitlines():
            pin,rel=line.split()
            src=repo/rel
            assert sha(src.read_bytes())==pin
            shutil.copyfile(src,stage/src.name)
            compile(src.read_bytes(),rel,"exec")
    enum=runpy.run_path(str(stage/"enumerate.py.txt"))
    product=runpy.run_path(str(stage/"product.py.txt"))
    s12=runpy.run_path(str(stage/"s12.py.txt"))
    store=runpy.run_path(str(stage/"capture.py.txt"))
    url=product["DEFAULT_PRODUCT"]
    qb="37777148";base=store["LIB"]["PREFIX"]+"20261113.1/"
    label=product["current_product"](url)
    xml=f"<build><id>{label}</id><base_repo>{base}</base_repo><buildconf_version>TIZEN_KantSU2E_Clang_build.conf@14452507</buildconf_version></build>".encode()
    original_cfg=stage/"K4.conf"
    old=url.replace("20261125.1","20261123.2")
    cfg_text=f"[repo.product_NikeM]\nurl = {old}\n[repo.base_standard]\nurl = {base}\n[profile.qb1111]\nbuildroot = /original\n"
    original_cfg.write_text(cfg_text)
    staged=enum["staged_config"](original_cfg,old,url,"/new")
    assert staged == cfg_text.replace(old,url).replace("/original","/new") and original_cfg.read_text()==cfg_text
    policy=product["check_publication"]
    policy(xml,url,base)
    for x,u in ((xml.replace(b"Clang_",b"GCC_"),url),(xml.replace(b"20261113.1",b"20261118.1"),url),
                (xml,"http://repos.vd.sec.samsung.net/products/tv/DO_NOT_DELETE/"+label+"/"),
                (xml,url.replace("20261125.1","20261123.2"))):
        try:policy(x,u,base)
        except ValueError:pass
        else:raise AssertionError(u)
    check=enum["check_inputs"]
    for bad,why in ((url+"builddata/build.xml","product-expired"),(base+"repodata/repomd.xml","deps")):
        def gone(*_):raise HTTPError(bad,404,"expired",None,None)
        out=io.StringIO()
        with patch.dict(check.__globals__,w=stage,preflight=gone),redirect_stdout(out):
            try:check({"repo.product_NikeM":url})
            except SystemExit as e:assert e.code==2
            else:raise AssertionError()
        assert "ENUM_RESULT SETUP_FAILED "+why in out.getvalue()
        assert ("NEED new LLVM Official QB product URL" in out.getvalue())==(why=="product-expired")
    # Shape of a legacy qb-retain capture: four kernel RPMs and primary, no filelists or external .ko RPM.
    cache=stage/"qb-evidence"
    folder=cache/(qb+"-"+label);folder.mkdir(parents=True)
    all_names=["tztv-kernel","tztv-kernel-perf","tztv-kernel-release","tztv-kernel-devel","external-module"]
    payloads={name:("fixture-"+name).encode() for name in all_names}
    primary=[];files=[]
    for name,blob in payloads.items():
        h=sha(blob);filename=name+".rpm"
        primary.append(f'<package><name>{name}</name><arch>armv7l</arch><checksum type="sha256">{h}</checksum><location href="{filename}"/></package>')
        f=f'<file>/lib/modules/perf/test/{name}.ko</file>' if name in ("tztv-kernel-perf","external-module") else ""
        files.append(f'<package pkgid="{h}" name="{name}" arch="armv7l">{f}</package>')
    streams={n:gzip.compress(("<metadata>"+"".join(v)+"</metadata>").encode()) for n,v in (("primary",primary),("filelists",files))}
    md=("<repomd>"+"".join(f'<data type="{n}"><location href="repodata/{n}.gz"/><checksum type="sha256">{sha(v)}</checksum></data>' for n,v in streams.items())+"</repomd>").encode()
    original={"build.xml":xml,"repomd.xml":md,"primary.download":streams["primary"]}
    for name in all_names[:4]:original[sha(payloads[name])[:16]+"-"+name+".rpm"]=payloads[name]
    for name,blob in original.items():(folder/name).write_bytes(blob)
    (folder/"identity.json").write_text(json.dumps(dict(product=url,qb_id_operator_supplied=qb,files={k:sha(v) for k,v in original.items()})))
    fetched=[]
    def fetch(u,_):
        fetched.append(u)
        if u.endswith("filelists.gz"):return streams["filelists"]
        if "/debug/" in u or "/debuginfo/" in u:raise HTTPError(u,404,"absent",None,None)
        if u.endswith("build.xml"):return xml
        if u.endswith("repomd.xml"):return md
        if u.endswith("primary.gz"):return streams["primary"]
        raise AssertionError(u)
    def rpm(pair,d):
        u,h=pair;f=d/u.rsplit("/",1)[-1]
        blob=payloads[f.stem]
        assert sha(blob)==h
        fetched.append(u);f.write_bytes(blob);return f
    fn=s12["retained_inputs"]
    for id in (qb,"38888888"):
        if id!=qb:
            url=url.replace("20261125.1","20261128.1")
            xml=xml.replace(b"20261125.1",b"20261128.1")
        work=stage/id;work.mkdir()
        with patch.dict(store["LIB"],fetch=fetch,cached_rpm=rpm),patch.dict(fn.__globals__,WS=stage),patch("runpy.run_path",return_value=store):
            rows,owners,paths=fn(id,url,qb,work)
            assert len(rows)==5 and len(owners)==2
            if id==qb:assert sum(u.endswith(".rpm") for u in fetched)==1
            else:assert sum(u.endswith(".rpm") for u in fetched)==5
            def offline(*args):raise AssertionError("unexpected network: "+str(args))
            with patch.dict(store["LIB"],fetch=offline,cached_rpm=offline):
                assert fn(id,url,qb,work)[0]==rows
                paths["external-module"].write_bytes(b"bad")
                try:fn(id,url,qb,work)
                except ValueError as exc:assert "checksum mismatch" in str(exc)
                else:raise AssertionError("accepted corrupted RPM")
        fetched.clear()
print("PASS publication, exact 404, launcher pins, legacy four-RPM import, external module, new QB retention, offline replay and corrupt cache")
