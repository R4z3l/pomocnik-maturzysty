import pymupdf,re,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a');out={}
for f in D.glob('uwr-*-plan.pdf'):
 n=f.stem.removesuffix('-plan');doc=pymupdf.open(f);gs=[]
 for p in list(doc)[:40 if n=='uwr-ekonomia' else 26 if n=='uwr-filozofia' else len(doc)]:
  ws=p.get_text('words');ss=[];lines=[]
  for dr in p.get_drawings():
   for it in dr['items']:
    if it[0]=='l' and abs(it[1].y-it[2].y)<.5:lines.append((min(it[1].x,it[2].x),max(it[1].x,it[2].x),it[1].y))
    elif it[0]=='re':lines.extend([(it[1].x0,it[1].x1,it[1].y0),(it[1].x0,it[1].x1,it[1].y1)])
  for w in ws:
   if w[4] not in ['O','W','OzW','Obowiązkowy','Wybieralny'] or not .1*p.rect.width<w[0]<.65*p.rect.width:continue
   # Boundaries must cross the name column and status column together.
   ys=sorted(set(round(y,2) for x0,x1,y in lines if x0<w[0]-30 and x1>w[0]+3))
   mid=(w[1]+w[3])/2;lower=[y for y in ys if y<mid];upper=[y for y in ys if y>mid]
   if not lower or not upper:continue
   y0,y1=lower[-1],upper[0]
   if not 6<y1-y0<150:continue
   # Keep words from the complete row; status itself defines name-column right edge.
   left=126 if w[4] in ['Obowiązkowy','Wybieralny'] else 0
   ww=[v for v in ws if left<v[0]<w[0]-3 and y0<(v[1]+v[3])/2<y1]
   v=' '.join(x[4] for x in sorted(ww,key=lambda x:(round(x[1]/3),x[0])))
   v=re.sub(r'^\d+\s+','',v);v=re.sub(r'\s+',' ',v).strip()
   if 3<len(v)<240 and not re.search(r'^(Nazwa|Suma|Razem|K_|SPECJALNOŚĆ)|ECTS|dyscyplina/punkty|INFORMACJE OGÓLNE',v,re.I):ss.append(v)
  if ss:gs.append({'page':p.number+1,'subjects':list(dict.fromkeys(ss))})
 out[n]=gs
 print(n,sum(len(g['subjects']) for g in gs),flush=True)
(D/'audited-geometry.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
