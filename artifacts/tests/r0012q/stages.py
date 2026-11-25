"""Replay four separate RPM shells with fresh environments and persistent cached driver paths."""
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile

art = Path(__file__).resolve().parents[2]
def load(p):
    return runpy.run_path(str(art/'scripts'/p))

def fixture(base, shell):
    dev = load('r0012/development.py.txt')
    matrix = load('r0012f/kernel-matrix.py.txt')
    tools = base/'bin'
    tools.mkdir()
    (tools/'bash').symlink_to(shell)
    for name in ('make','clang','clang++','armv7l-tizen-linux-gnueabi-clang','armv7l-tizen-linux-gnueabi-clang++','cc','c++','ld.lld'):
        p=tools/name
        p.write_text('#!/bin/sh\ncase "$1" in -###|--version) echo fixture;; esac\n')
        p.chmod(0o755)
    env={'PATH':str(tools)+':'+os.environ['PATH'],'LC_ALL':'C','HOME':str(base)}
    for kind in ('package','kernel'):
        root=base/kind
        root.mkdir()
        stages=('prep','build','install','check')
        spec=''.join('%'+stage+'\n# stage body\n' for stage in stages)
        if kind=='package':
            gen=dev['hook_source']((art/'scripts/r0012m/observe-driver.sh.txt').read_text(),dev['EMPTY'])
            gen=gen.replace('export PATH="$pm12_bin:$PATH"',dev['GCC_TRACE']+'export PATH="$pm12_bin:$PATH"')
            spec=dev['rpm_stage_tools'](spec,'%{_builddir}/.pm12-driver',dev['thumb_stage_setup'](gen))
            names=['armv7l-tizen-linux-gnueabi-clang++','cc']
        else:
            p=root/'spec'
            p.write_text(spec.replace('%build\n','%build\n'+load('r0008a/gbs-mlgo-t7.py.txt')['INSTRUMENT']))
            subprocess.run(['patch','--fuzz=0','--batch',p,art/'patches/kernel/perf-machine-outliner.spec.patch'],check=True)
            spec=matrix['stage_spec'](p.read_text(),'K1',dev)
            names=['clang','make','ld.lld']
        for stage,body in zip(stages,re.split(r'(?m)^%(?:prep|build|install|check)\n',spec)[1:]):
            cwd=root/stage
            cwd.mkdir()
            for name in names:
                absolute=root/('.pm12-driver' if kind=='package' else '.pm0012f-tools')/name
                body+=f'\ntest "$(command -v {name})" = "{absolute}" || exit 2\n'
                body+=f'"{absolute}" sample.o "-DKEEP=two words" -o sample\n'
            result=subprocess.run([shell,'-eu'],input=body.replace('%{_builddir}',str(root)).replace('%%','%'),
                cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            if result.returncode:
                raise AssertionError((kind,stage,result.stdout[-2000:]))
        if kind=='package':
            records=[p.read_text() for p in (root/'.pm12-driver/receipts').glob('driver.*')]
            for stage in stages:
                matching=[s for s in records if 'PM12_STAGE '+stage+'\n' in s]
                assert len(matching)==2 and any('PM_GCC_ARGV' in s for s in matching)
                assert any('PM12_DRIVER link' in s and 'two\\ words' in s for s in matching)
        # Exercise RPM's own percent expansion, fresh shell macros and builddir, too.
        spec=spec.replace('# stage body', 'test "${BASH_VERSION%%.*}" = 3 || exit 2\n'
                          + '\n'.join(n+' stage-input.o -o output' for n in names))
        # The synthetic kernel %build preamble queries the RPM database. Use
        # the stand-in database responder for the fixture build only.
        rpmstub=tools/'rpm'
        rpmstub.write_text('#!/bin/sh\nexit 0\n')
        rpmstub.chmod(0o755)
        spec=spec.replace('${BASH_VERSION%%.*}', '${BASH_VERSION%%%%.*}')
        top=root/'top'
        for n in ('BUILD','BUILDROOT','RPMS','SOURCES','SPECS','SRPMS','tmp','db'):
            (top/n).mkdir(parents=True,exist_ok=True)
        package=top/'SPECS/probe.spec'
        package.write_text('Name: stage-probe\nVersion: 1\nRelease: 1\nSummary: Stage fixture\n'
                           'License: MIT\n%description\nStage fixture\n'+spec+'\n%files\n')
        args=['rpmbuild','-bb','--nodeps']
        for key,value in [('_topdir',top),('_tmppath',top/'tmp'),('_dbpath',top/'db'),
                          ('_buildshell',shell),('__os_install_post','%{nil}')]:
            args.extend(['--define',f'{key} {value}'])
        result=subprocess.run([*args,package],env={**env,'TMPDIR':str(top/'tmp')},text=True,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        if result.returncode: raise AssertionError(result.stdout[-3000:])
        print('PASS',kind,'rpmbuild -bb with real Bash 3.2 at all four stage entries')
        print('PASS',kind,'prep build install check, fresh Bash 3.2 shells; cached paths from distinct cwd')
with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as d:
    bash=Path(sys.argv[1]).resolve()
    assert subprocess.check_output([bash,'-c','echo "$BASH_VERSION"'],text=True).startswith('3.2.57')
    fixture(Path(d),bash)
