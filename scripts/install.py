"""Install the complete local skill. Does not fetch code, change host permissions, or require keys."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import tempfile
from check_package import check

def install(source,skills_root,update=False):
    source=Path(source).resolve()
    skills_root=Path(skills_root).expanduser().resolve()
    dest=skills_root/'xuxiaoyu-skill'
    if dest.is_symlink():raise ValueError('Target is a symlink; choose a normal skill directory.')
    if dest.resolve()==source or dest.resolve().is_relative_to(source):
        raise ValueError('Target must be outside the source package.')
    check(source)
    if dest.exists() and not update:raise ValueError('Already installed. Use --update to back up and replace it.')
    skills_root.mkdir(parents=True,exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.xuxiaoyu-install-',dir=skills_root))
    backup=None
    try:
        manifest=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
        for rel in [*manifest['files'],'manifest.json']:
            p=stage/rel;p.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source/rel,p)
            p.chmod(0o644)
        for p in stage.rglob('*'):
            if p.is_dir():p.chmod(0o755)
        stage.chmod(0o755)
        check(stage)
        if dest.exists():
            backups=skills_root.parent/'skill-backups';backups.mkdir(parents=True,exist_ok=True)
            backup=backups/('xuxiaoyu-skill-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
            os.replace(dest,backup)
        try:os.replace(stage,dest)
        except OSError:
            if backup is not None:os.replace(backup,dest)
            raise
        return {'installed':str(dest),'backup':str(backup) if backup else None,'chat':'$xuxiaoyu-skill 我想和你聊聊我的项目。'}
    finally:
        if stage.exists():shutil.rmtree(stage)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Install xuxiaoyu-skill locally; Python 3.9+ only, no pip packages.')
    parser.add_argument('--agent',choices=['codex','claude','cursor'],default='codex')
    parser.add_argument('--target',type=Path,help='Parent skill directory; installation creates xuxiaoyu-skill inside it.')
    parser.add_argument('--update',action='store_true',help='Back up an existing install before replacing it.')
    args=parser.parse_args()
    roots={'codex':'.agents/skills','claude':'.claude/skills','cursor':'.cursor/skills'}
    try:
        print(json.dumps(install(Path(__file__).resolve().parent.parent,args.target or Path.home()/roots[args.agent],args.update),ensure_ascii=False,indent=2))
    except (OSError,ValueError,KeyError) as exc:parser.exit(1,'Installation failed: '+str(exc)+'\n')
