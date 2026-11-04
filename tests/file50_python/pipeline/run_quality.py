"""Portable runner for reviewed campaign contracts only; no global installation."""
import argparse,json,os,subprocess,sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);parser.add_argument('--coverage',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parents[3];out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);tmp=out/'tmp';tmp.mkdir(exist_ok=True)
    # Previous invocation evidence is never current evidence.
    artifacts = ('.coverage', '.coverage-journal', '.coverage-shm', '.coverage-wal', 'command.json', 'coverage-export.log', 'coverage.json', 'exit-code.json', 'junit.xml', 'runtime.log')
    previous = [(out / name) for name in artifacts if (out / name).is_file()]
    if previous:
        import tempfile
        archive = Path(tempfile.mkdtemp(prefix="previous-", dir=str(out)))
        for path in previous:
            path.replace(archive / path.name)
    config=json.loads(Path(__file__).with_name('quality_scope.json').read_text())
    if not config['tests']:
        raise ValueError('quality_scope.json must select at least one test')
    extra=os.environ.get('PIPELINE_EXTRA_PYTHONPATH','')
    paths=[str(root),str(Path(__file__).parent)]+[str(root/p) for p in config['import_paths']]+([extra] if extra else [])
    env={'PATH':os.environ.get('PATH','/usr/bin:/bin'),'LANG':'C.UTF-8','PYTHONPATH':os.pathsep.join(paths),'PYTHONDONTWRITEBYTECODE':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','AWS_EC2_METADATA_DISABLED':'true','PROJ_NETWORK':'OFF','TMPDIR':str(tmp),'OFFLINE_OUTPUT':str(out),'COVERAGE_FILE':str(out/'.coverage')}
    env.update(config.get('synthetic_environment',{}))
    if config.get('dependency_root'):env['OFFLINE_DEPENDENCY_ROOT']=str(root/config['dependency_root'])
    cmd=[sys.executable,'-m']
    if args.coverage:cmd+=['coverage','run','--source='+','.join(config['source_roots']),'-m']
    cmd+=['pytest','-c','/dev/null','--rootdir='+str(root),'--import-mode=importlib','--tb=short','-q']
    for plugin in ['quality_guard']+config['plugins']:cmd+=['-p',plugin]
    cmd+=config['tests']+['--junitxml='+str(out/'junit.xml')]
    (out/'command.json').write_text(json.dumps({'argv':cmd,'cwd':str(root),'environment':env},indent=2)+'\n')
    with (out/'runtime.log').open('w') as log:r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
    if args.coverage:
        with (out/'coverage-export.log').open('w') as log:exported=subprocess.run([sys.executable,'-m','coverage','json','-o',str(out/'coverage.json')],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
    exit_code = r.returncode or (exported.returncode if args.coverage else 0)
    (out / 'exit-code.json').write_text(json.dumps({'exit_code': exit_code, 'test_exit_code': r.returncode, 'coverage_exit_code': exported.returncode if args.coverage else None}) + '\n')
    return exit_code
if __name__=='__main__':raise SystemExit(main())
