import pymupdf,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a')
for n,f,pg in [('admin','law-combined-plan.pdf',0),('BBA','uwr-bachelor-of-business-and-administration-plan.pdf',58),('CJ','uwr-criminal-justice-plan.pdf',1),('dz','uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie-plan.pdf',0),('ek','uwr-ekonomia-plan.pdf',30)]:
 d=pymupdf.open(D/f);p=d[pg];print(n,flush=True)
 print([[p.get_textbox(c).replace('\n',' ') if c else '' for c in r.cells] for r in p.find_tables().tables[0].rows[:7]],flush=True)
