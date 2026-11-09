import pymupdf,json,re,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a');out={}
for pid,file,pages in [('uwr-administracja','law-combined-plan.pdf',range(0,5)),('uwr-criminal-justice','uwr-criminal-justice-plan.pdf',range(1,5)),('uwr-bachelor-of-business-and-administration','uwr-bachelor-of-business-and-administration-plan.pdf',range(58,65)),('uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie','uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie-plan.pdf',range(0,5))]:
 d=pymupdf.open(D/file);gs=[]
 for i in pages:
  p=d[i];p.remove_rotation();ss=[]
  for tb in p.find_tables().tables:
   for row in tb.rows:
    vs=[re.sub(r'\s+',' ',p.get_textbox(c)).strip() if c else '' for c in row.cells]
    if len(vs)<3:continue
    # Known plans have name as second column, Lp. as first; blanks continue elective rows.
    v=vs[1]
    if not v or len(v)>220 or re.search(r'^(Nazwa|Przedmiot$|Przedmioty|Razem|Wskaźniki|Liczba|Specjalność|bezpieczeństwo wewnętrzne$|administracja europejska$|samorząd terytorialny$|administracja sektora publicznego$)|ECTS|dyscyplina/punkty',v,re.I):continue
    if not re.fullmatch(r'\d+[.\s]*|',vs[0]):continue
    if not any(re.search(r'\d|E/Z|zal',x,re.I) for x in vs[2:]):continue
    ss.append(v)
  if ss:gs.append({'page':i+1,'subjects':list(dict.fromkeys(ss))})
 out[pid]=gs;print(pid,sum(len(g['subjects']) for g in gs),flush=True)
 (D/'audited-simple.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
