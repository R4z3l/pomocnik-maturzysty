from pathlib import Path
import json,re,collections,importlib.util
import pymupdf as f
root=Path(__file__).parent/'cache'
spec=importlib.util.spec_from_file_location('extr',Path(__file__).parent/'extract.py');extr=importlib.util.module_from_spec(spec);spec.loader.exec_module(extr)
keys=['1bea8d0e31c7f84c','1e2369b8d0556be9','21cdfea431c48440','32a44938069e16f8','55e9b9ae113f7a2d','607848dedc3157d7','687a6cc41b1b467d','76b40106fea15ebb','91f0c5c9c783c128','9babb9732af227db','9ee9faa1cb067728','add6d4e3c4f0027a','addb3d02c585ebb3','cf727cf4e9724481','f53546919a57ada9','ff5924209372dc9d']
extr.configs.update({'56931a4e3c053d65':range(1,8),'0a82482251f76c17':range(44,78),'2b5b748ee09d20ad':range(28,33),'7eb11fdf0ed64f2d':range(31,36),'8aa125798454591a':range(2,18)})
keys+=['56931a4e3c053d65','0a82482251f76c17','2b5b748ee09d20ad','7eb11fdf0ed64f2d','8aa125798454591a']
for key in keys:
 doc=f.open(root/(key+'.pdf'));out=[];pages=extr.configs[key]
 if key=='55e9b9ae113f7a2d':pages=range(12,17)
 for n in pages:
  if n>len(doc):continue
  p=doc[n-1];ws=p.get_text('words');raw=[w for w in ws if re.fullmatch('O|F|OzW|OF|W|Obowiązkowy|Wybieralny',w[4])];
  if not raw:continue
  freq=collections.Counter(round(w[0]) for w in raw);x=freq.most_common(1)[0][0]
  left=28;usos=any(w[4]=='Obowiązkowy' for w in raw)
  if usos:
   headers=[w for w in ws if w[4]=='przedmiotu' and w[1]<120]
   if headers:left=headers[0][0]-10
  anchors=sorted([w for w in raw if abs(w[0]-x)<20],key=lambda w:w[1]);names=[]
  rules=[];mid=(35+x)/2;horizontal=[];vertical=[]
  for drawing in p.get_drawings():
   for item in drawing['items']:
    if item[0]=='re':
     rr=item[1]
     if rr.width<1.2 and rr.height>3:vertical.append((rr.x0,rr.y0,rr.y1))
     if rr.height<1.2 and rr.width>3:horizontal.append((rr.y0,rr.x0,rr.x1))
     if rr.height<1.2 and rr.x0<mid<rr.x1:rules.append(rr.y0)
    elif item[0]=='l' and abs(item[1].y-item[2].y)<1 and min(item[1].x,item[2].x)<mid<max(item[1].x,item[2].x):rules.append(item[1].y)
  rules=sorted(set(round(y,1) for y in rules))
  for i,a in enumerate(anchors):
   center=(a[1]+a[3])/2
   vx=sorted(set(round(v[0]) for v in vertical if v[1]<center<v[2] and v[0]<a[0]-2))
   rowleft=left;rowright=x-2
   if len(vx)>=2 and not usos:
    rowright=vx[-1];prev=[v for v in vx if v<rowright-3]
    if prev:rowleft=prev[-1]-1
   localrules=[h[0] for h in horizontal if h[1]<(rowleft+rowright)/2<h[2]]
   if localrules and not usos:rules=sorted(set(round(y,1) for y in localrules))
   before=[y for y in rules if y<center];after=[y for y in rules if y>center]
   y0=max(before) if before else a[1]-1;y1=min(after) if after else (anchors[i+1][1]-1 if i+1<len(anchors) else a[1]+55)
   if usos:
    y0=a[1]-1;y1=anchors[i+1][1]-1 if i+1<len(anchors) else a[1]+55
    sums=[w[1] for w in ws if w[4]=='SUMA' and a[1]<w[1]<y1]
    if sums:y1=min(sums)
   if y1-y0>150:continue
   words=sorted([w for w in ws if w[0]>rowleft and w[2]<rowright+1 and y0<=w[1]<y1],key=lambda w:(round(w[1]/2),w[0]))
   name=extr.clean(' '.join(w[4] for w in words));name=re.split(r'SUMA|Razem|Łączna|Wykaz przedmiotów|\*\*\*|ROK STUDIÓW|SEMESTR|Nazwa przedmiotu|Objaśnienia|Wskaźniki',name)[0].strip()
   name=re.sub(r'^\d+[.]?\s*','',name)
   if len(name)>3 and 'RAZEM MODUŁ' not in name:names.append(name)
  out.append({'page':n,'context':extr.clean(p.get_text()[:180]),'subjects':names})
 (root/(key+'.selected.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(key,sum(len(g['subjects']) for g in out))
