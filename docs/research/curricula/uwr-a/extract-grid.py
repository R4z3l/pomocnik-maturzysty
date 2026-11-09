import pymupdf,re,json,sys
from pathlib import Path
D=Path('docs/research/curricula/uwr-a');sys.stdout.reconfigure(encoding='utf-8')
out={}
for pp in D.glob('uwr-*-plan.pdf'):
 n=pp.stem.removesuffix('-plan');doc=pymupdf.open(pp);groups=[]
 maxp=40 if n=='uwr-ekonomia' else 26 if n=='uwr-filozofia' else len(doc)
 for p in list(doc)[:maxp]:
  spans=[s for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']];ws=p.get_text('words');draw=p.get_drawings();ys=[]
  for d in draw:
   for it in d['items']:
    if it[0]=='l' and abs(it[1].y-it[2].y)<.5 and abs(it[1].x-it[2].x)>100:ys.append(it[1].y)
    if it[0]=='re':ys.extend([it[1].y0,it[1].y1])
  ys=sorted(set(round(y,1) for y in ys));subs=[]
  for w in ws:
   if w[4] not in ['O','OzW','W','Obowiązkowy','Wybieralny'] or not .07*p.rect.width<w[0]<.65*p.rect.width:continue
   prev=[y for y in ys if y<w[1]+1];nxt=[y for y in ys if y>w[3]-1]
   if not prev or not nxt:continue
   y0,y1=prev[-1],nxt[0]
   if y1-y0>100 or y1-y0<5:continue
   left=[s for s in spans if (126 if w[4] in ['Obowiązkowy','Wybieralny'] else 0)<s['bbox'][0]<w[0]-3 and y0-1<s['bbox'][1]<y1-2 and len(s['text'].strip())>1]
   ls=[s['text'].strip() for s in sorted(left,key=lambda s:(round(s['bbox'][1]),s['bbox'][0])) if not re.fullmatch(r'[\d\s.,%+–-]+',s['text'].strip())]
   v=' '.join(ls);v=re.sub(r'\s+',' ',v).strip()
   if 4<len(v)<230 and not re.search(r'Nazwa|Liczba godzin|Wydział|ECTS|Jednostka|Forma zajęć|The discipline|kursu odnosi|Sposób|zawodowy|humanistyczne|Dziedzina|ogólnoakademicki',v,re.I):subs.append(v)
  if subs:groups.append({'page':p.number+1,'semester':None,'subjects':list(dict.fromkeys(subs))})
 out[n]=groups;print(n,sum(len(g['subjects']) for g in groups),flush=True)
 (D/'extracted-grid.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
