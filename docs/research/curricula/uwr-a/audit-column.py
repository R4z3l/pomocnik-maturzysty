import pymupdf,json,re,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a');out={}
for pid,file,pages,x0,x1 in [('uwr-administracja','law-combined-plan.pdf',range(0,5),53,249),('uwr-criminal-justice','uwr-criminal-justice-plan.pdf',range(1,5),59,238),('uwr-bachelor-of-business-and-administration','uwr-bachelor-of-business-and-administration-plan.pdf',range(58,65),54,270),('uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie','uwr-dziedzictwo-kultury-materialnej-ochrona-promocja-gospodarowanie-plan.pdf',range(0,5),90,243)]:
 d=pymupdf.open(D/file);gs=[]
 for i in pages:
  p=d[i];p.remove_rotation();ss=[];ys=[];mid=(x0+x1)/2
  for dr in p.get_drawings():
   for it in dr['items']:
    if it[0]=='l' and abs(it[1].y-it[2].y)<.5 and min(it[1].x,it[2].x)<mid<max(it[1].x,it[2].x):ys.append(it[1].y)
    elif it[0]=='re' and it[1].x0<mid<it[1].x1:ys.extend([it[1].y0,it[1].y1])
  ys=sorted(set(round(y,1) for y in ys));ys=[y for j,y in enumerate(ys) if j==0 or y-ys[j-1]>3];ws=p.get_text('words')
  for ya,yb in zip(ys,ys[1:]):
   if yb-ya<7:continue
   ww=[w for w in ws if x0<(w[0]+w[2])/2<x1 and ya<(w[1]+w[3])/2<yb]
   v=' '.join(w[4] for w in sorted(ww,key=lambda w:(round(w[1]/3),w[0]))).strip()
   if 3<len(v)<240 and not re.search(r'^(Nazwa|Przedmiot$|Przedmioty|Razem|Wskaźniki|Liczba|Specjalność|Przedmiot do wyboru \(jeden)|ECTS|dyscyplina/punkty|Forma|Godzin|Suma|PROGRAM|Wykład|Jednostka',v,re.I):ss.append(v)
  if ss:gs.append({'page':i+1,'subjects':list(dict.fromkeys(ss))})
 out[pid]=gs;print(pid,sum(len(g['subjects']) for g in gs),flush=True)
(D/'audited-column.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
