import json,re,pymupdf,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a');out={}
ids=['analityka-spoleczna','anglistyka','chemia','chemia-medyczna','chemistry','culture-thought-and-humanity','data-and-society','edukacja-polonistyczna-current','etnologia-i-antropologia-kulturowa','etyka','europeistyka','filologia-chorwacka-z-jezykiem-serbskim','filologia-czeska','filologia-francuska','filologia-germanska','filologia-hiszpanska','filologia-indyjska','filologia-klasyczna','filologia-polska','filologia-rosyjska','filologia-ukrainska']
for n in ids:
 f=D/('uwr-'+n+'-plan.pdf')
 if not f.exists():continue
 doc=pymupdf.open(f);gs=[]
 for p in doc:
  ss=[]
  for tb in p.find_tables().tables:
   for row in tb.rows:
    vs=[re.sub(r'\s+',' ',p.get_textbox(c)).strip() if c else '' for c in row.cells]
    for j,v in enumerate(vs):
     if j and re.fullmatch(r'O|W|OzW|Obowiązkowy|Wybieralny',v):
      # Course cell immediately precedes obligatory/elective indicator; merged placeholders are empty.
      prev=next((x for x in reversed(vs[:j]) if x),'')
      if len(prev)>3 and len(prev)<240 and not re.search(r'^(Nazwa|Suma|Razem|SPECJALNOŚĆ|Moduł nauczycielski)|ECTS|dyscyplina/punkty',prev,re.I):ss.append(prev)
  if ss:gs.append({'page':p.number+1,'subjects':list(dict.fromkeys(ss))})
 out['uwr-'+n]=gs
 (D/'audited-cells.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
 print(n,sum(len(g['subjects']) for g in gs),flush=True)
