"""Portable runner for reviewed campaign contracts only; no global installation."""
import argparse,json,os,subprocess,sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);parser.add_argument('--coverage',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parents[3];out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);tmp=out/'tmp';tmp.mkdir(exist_ok=True)
    config=json.loads(Path(__file__).with_name('quality_scope.json').read_text())
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
        with (out/'coverage-export.log').open('w') as log:subprocess.run([sys.executable,'-m','coverage','json','-o',str(out/'coverage.json')],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    (out/'exit-code.json').write_text(json.dumps({'exit_code':r.returncode})+'\n');return r.returncode
if __name__=='__main__':raise SystemExit(main())
