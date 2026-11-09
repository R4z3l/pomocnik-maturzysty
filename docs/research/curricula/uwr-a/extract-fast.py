import pymupdf,re,json,sys
from pathlib import Path
D=Path('docs/research/curricula/uwr-a');sys.stdout.reconfigure(encoding='utf-8');out={}
for n in ['uwr-fizyka','uwr-astronomia','uwr-geoinformacja','uwr-geografia']:
 doc=pymupdf.open(D/(n+'-plan.pdf'));groups={}
 for p in doc:
  ls=[x.strip() for x in p.get_text().splitlines() if x.strip()]
  for i,x in enumerate(ls):
   m=re.fullmatch(r'(?:E/Z|Z|E|Z/Z|ZAL)(?:\s*\(([IVX,\s–-]+)\))',x)
   if m:
    prev=[]
    for v in reversed(ls[max(0,i-4):i]):
     if re.fullmatch(r'[\d\s.,/–-]+',v) or 'tok ' in v.lower() or 'SEMESTR' in v or 'ECTS' in v:break
     prev.insert(0,v)
    sub=' '.join(prev)
    if sub and len(sub)<180:groups.setdefault(m.group(1),[]).append(sub)
   if n in ['uwr-geoinformacja','uwr-geografia'] and x.isdigit() and i+3<len(ls) and re.match(r'^[A-ZĄĆĘŁŃÓŚŹŻ]',ls[i+1]):
    words=[];j=i+1
    while j<len(ls) and not re.fullmatch(r'[\d.]+',ls[j]) and len(words)<4:words.append(ls[j]);j+=1
    if j+1<len(ls) and ls[j+1] in ['z','E','Z']:groups.setdefault(None,[]).append(' '.join(words))
 out[n]=[{'semester':k,'subjects':list(dict.fromkeys(v))} for k,v in groups.items()]
 print(n,sum(len(g['subjects']) for g in out[n]),out[n][:1])
# Philosophy: the first 26 pages belong to full-time first-cycle studies.
n='uwr-filozofia';doc=pymupdf.open(D/(n+'-plan.pdf'));subs=[]
for p in list(doc)[20:26]:
 for b in p.get_text('dict')['blocks']:
  ss=[s['text'].strip() for l in b.get('lines',[]) for s in l['spans'] if 120<s['bbox'][0]<185 and s['bbox'][1]>110]
  v=' '.join(ss)
  if len(v)>3 and not re.search(r'RAZEM|SUMA|\[h\]|ECTS|przedmiotu|Obowiązkowy|Wybieralny',v):subs.append(v)
out[n]=[{'semester':None,'subjects':list(dict.fromkeys(subs))}];print(n,out[n])
(D/'extracted-fast.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
