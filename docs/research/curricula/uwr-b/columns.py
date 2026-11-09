import json,re
from pathlib import Path
import pymupdf as f
root=Path(__file__).parent/'cache'
def clean(t):return re.sub(r'\s+',' ',t).strip()
def anchored(key,pages,namex,anchorx,pattern,offset=-1):
 doc=f.open(root/(key+'.pdf'));out=[]
 for n in pages:
  p=doc[n-1];ws=p.get_text('words');anchors=[w for w in ws if anchorx[0]<=w[0]<=anchorx[1] and re.fullmatch(pattern,w[4])];anchors.sort(key=lambda w:w[1]);names=[]
  for i,a in enumerate(anchors):
   y0=a[1]+offset
   y1=anchors[i+1][1]+offset if i+1<len(anchors) else a[1]+55
   words=[w for w in ws if namex[0]<=w[0] and w[2]<=namex[1] and y0<=w[1]<y1]
   words.sort(key=lambda w:(round(w[1]/2),w[0]));name=clean(' '.join(w[4] for w in words))
   name=re.split(r'SUMA|Razem:|NAZWA PRZEDMIOTU|Nazwa przedmiotu|Liczba egzaminów|Przedmioty do wyboru za|Przygotowanie pracy licencjackiej \(do wyboru\)',name)[0].strip()
   if name:names.append(name)
  out.append({'page':n,'context':clean(p.get_text()[:180]),'subjects':names})
 (root/(key+'.selected.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
 print(key,len([s for g in out for s in g['subjects']]))
def blocks(key,pages,namex):
 doc=f.open(root/(key+'.pdf'));out=[]
 for n in pages:
  p=doc[n-1];names=[]
  for b in p.get_text('blocks',clip=f.Rect(namex[0],0,namex[1],p.rect.height)):
   name=clean(b[4])
   if len(name)>4 and not any(t in name.lower() for t in ['nazwa przedmiotu','semestr:','rok studiów','suma','literatura światowa:','razem','program studiów','ects','przedmiot z/e','uwaga','*']):names.append(name)
  out.append({'page':n,'context':clean(p.get_text()[:180]),'subjects':names})
 (root/(key+'.selected.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
 print(key,len([s for g in out for s in g['subjects']]))
anchored('b2b22700aa9f6414',range(2,8),(45,195),(195,215),'O|OzW|F')
anchored('989700773cd625a0',range(2,10),(45,195),(195,215),'O|OzW|F')
anchored('c559d1ef651e1996',[1,2],(20,240),(275,290),'E|Z',-5)
anchored('95723042531130d5',[1,2],(20,250),(285,300),'E|Z',-5)
anchored('7eb11fdf0ed64f2d',range(31,36),(105,161),(163,210),'Obowiązkowy|Wybieralny')
blocks('e4ae0e1cd09b1f6c',range(1,6),(68,350))
blocks('e37a3a33da818877',range(1,4),(68,253))
