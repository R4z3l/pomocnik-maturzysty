import pymupdf,json,re,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a')
results={}
for p in D.glob('uwr-*-plan.pdf'):
 doc=pymupdf.open(p);groups=[];lastidx=None;lastcols=None
 maxpages=40 if p.stem=='uwr-ekonomia-plan' else len(doc)
 for pg in list(doc)[:maxpages]:
  txt=pg.get_text();sem=re.findall(r'[Ss][Ee][Mm][Ee][Ss][Tt][Rr]\s*:?\s*(pierwszy|drugi|trzeci|czwarty|piąty|szósty|\d+|I{1,3}V?|V?I{0,3})\b',txt);sem=sem[0] if sem else None
  for tb in pg.find_tables().tables:
   rows=tb.extract();idx=None;header=-1
   for i,row in enumerate(rows[:4]):
    for j,c in enumerate(row):
     if c and re.search(r'nazwa\s*przedmiotu',c,re.I):idx=j;header=i;break
    if idx is not None:break
   if idx is None:continue
   subs=[]
   for row in rows[header+1:]:
    if idx>=len(row) or not row[idx]:continue
    v=re.sub(r'\s+',' ',row[idx]).strip();v=re.sub(r'^\d+\.\s*','',v)
    if len(v)<4 or re.search(r'^(suma|razem|liczba|ects|nazwa|treści|ogółem|uwagi|sposób|forma|semestr|przedmiot/moduł)',v,re.I):continue
    if len(v)>220:continue
    if v.endswith(' –'):v=v[:-2]
    subs.append(v)
   if subs:groups.append({'page':pg.number+1,'semester':sem,'subjects':list(dict.fromkeys(subs))})
 results[p.stem.removesuffix('-plan')]=groups
 print(p.stem,sum(len(g['subjects']) for g in groups),flush=True)
(D/'extracted-tables.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
