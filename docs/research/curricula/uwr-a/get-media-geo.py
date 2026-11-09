import sys,json,subprocess,io,zipfile
from pathlib import Path
sys.path.insert(0,'scripts');from source_policy import guarded_get
D=Path('docs/research/curricula/uwr-a');sys.stdout.reconfigure(encoding='utf-8')
jobs=[('media-cw','https://idiks.uwr.edu.pl/wp-content/uploads/sites/576/2024/10/CW_programy.zip'),('media-mcc','https://idiks.uwr.edu.pl/wp-content/uploads/sites/576/2024/10/MCC_programy.zip'),('media-da','https://idiks.uwr.edu.pl/wp-content/uploads/sites/576/2024/10/DA_programy.zip'),('geologia','https://ing.uwr.edu.pl/wp-content/uploads/sites/64/2023/02/lib-geologia-i-st-plan-studiow-od-2022_2023.xls')]
for name,u in jobs:
 subprocess.run(['node','--experimental-strip-types','scripts/check-source.ts',u,'current'],check=True,capture_output=True);r=guarded_get(u);(D/(name+('.xls' if name=='geologia' else '.zip'))).write_bytes(r.content)
 if name!='geologia':
  z=zipfile.ZipFile(io.BytesIO(r.content));print(name,z.namelist());od=D/name;od.mkdir(exist_ok=True)
  for f in z.infolist():
   if not f.is_dir():(od/Path(f.filename).name).write_bytes(z.read(f))
