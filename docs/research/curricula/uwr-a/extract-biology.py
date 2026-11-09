import json,pymupdf,re,sys
from pathlib import Path
D=Path('docs/research/curricula/uwr-a');out={};sys.stdout.reconfigure(encoding='utf-8')
for n in ['uwr-biologia','uwr-biologia-czlowieka','uwr-genetyka-i-biologia-eksperymentalna','uwr-genetics-and-experimental-biology']:
 groups={};doc=pymupdf.open(D/(n+'-plan.pdf'))
 for pg in doc:
  spans=[s for b in pg.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
  headings=[]
  for b in pg.get_text('dict')['blocks']:
   for l in b.get('lines',[]):
    t=' '.join(s['text'] for s in l['spans']);m=re.search(r'SEMESTR\s*(\d+)',t,re.I)
    if m:headings.append((l['bbox'][1],m.group(1)))
  anchors=[s for s in spans if re.search(r'25-[A-Z]+-S1-E[1-6]-|00-BHP|8545-WF|60-S',s['text'])]
  for a in anchors:
   left=[s for s in spans if s['bbox'][0]<200 and s['bbox'][2]<250 and a['bbox'][1]-8<=s['bbox'][1]<=a['bbox'][1]+1.8 and len(s['text'].strip())>3]
   left=[s for s in left if not any(w in s['text'] for w in ['Przedmioty obowiązkowe','SEMESTR','ECTS','Razem:'])]
   if not left:continue
   v=' '.join(s['text'].strip() for s in sorted(left,key=lambda s:s['bbox'][1]));v=v.strip('* ')
   before=[h for h in headings if h[0]<a['bbox'][1]]
   sem=before[-1][1] if before else re.search(r'-E([1-6])-',a['text']).group(1) if re.search(r'-E([1-6])-',a['text']) else None
   groups.setdefault(sem,[]).append(v)
 out[n]=[{'semester':k,'subjects':list(dict.fromkeys(v))} for k,v in groups.items()]
 print(n,sum(len(g['subjects']) for g in out[n]),out[n][0])
(D/'extracted-biology.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
