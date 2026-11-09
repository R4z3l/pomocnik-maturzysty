import pymupdf,json,re,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a');out={}
for f in D.glob('uwr-*-plan.pdf'):
 n=f.stem.removesuffix('-plan');d=pymupdf.open(f);gs=[]
 for p in list(d)[:40 if n=='uwr-ekonomia' else 26 if n=='uwr-filozofia' else len(d)]:
  ws=p.get_text('words');h=[];vert=[];ss=[]
  for dr in p.get_drawings():
   for it in dr['items']:
    if it[0]=='l':
     a,b=it[1],it[2]
     if abs(a.y-b.y)<.5:h.append((min(a.x,b.x),max(a.x,b.x),a.y))
     if abs(a.x-b.x)<.5:vert.append((a.x,min(a.y,b.y),max(a.y,b.y)))
    elif it[0]=='re':
     r=it[1];h.extend([(r.x0,r.x1,r.y0),(r.x0,r.x1,r.y1)]);vert.extend([(r.x0,r.y0,r.y1),(r.x1,r.y0,r.y1)])
  for w in ws:
   if w[4] not in ['O','W','OzW','Obowiązkowy','Wybieralny']:continue
   ym=(w[1]+w[3])/2;xm=(w[0]+w[2])/2
   xs=sorted(set(round(x,1) for x,y0,y1 in vert if y0-1<ym<y1+1 and x<xm))
   xs=[x for i,x in enumerate(xs) if i==0 or x-xs[i-1]>3]
   if len(xs)<2:continue
   x0,x1=xs[-2:];mid=(x0+x1)/2
   if x1-x0<40:continue
   ys=sorted(set(round(y,1) for a,b,y in h if a-.5<mid<b+.5));lo=[y for y in ys if y<ym];hi=[y for y in ys if y>ym]
   if not lo or not hi:continue
   y0,y1=lo[-1],hi[0]
   if not 5<y1-y0<180:continue
   ww=[v for v in ws if x0<(v[0]+v[2])/2<x1 and y0<(v[1]+v[3])/2<y1]
   v=' '.join(a[4] for a in sorted(ww,key=lambda a:(round(a[1]/3),a[0])))
   if 3<len(v)<220 and not re.search(r'^(Nazwa|Razem|SUMA|SPECJALNOŚĆ|K_)|ECTS|dyscyplina/punkty',v,re.I):ss.append(v)
  if ss:gs.append({'page':p.number+1,'subjects':list(dict.fromkeys(ss))})
 out[n]=gs;print(n,sum(len(g['subjects']) for g in gs),flush=True)
(D/'audited-rectangles.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
