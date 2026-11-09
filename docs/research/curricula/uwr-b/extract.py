from pathlib import Path
import json,re,concurrent.futures
import pymupdf as fitz
root=Path(__file__).parent/'cache'
# Only pages containing the course plan (not outcomes, reading lists or another degree).
configs={
'04781d78c4e3569e':list(range(16,20)),
'17e1456c2be5f03a':list(range(19,26)),
'1bea8d0e31c7f84c':list(range(1,11)),
'1e2369b8d0556be9':list(range(67,86)),
'21cdfea431c48440':list(range(17,25)),
'32a44938069e16f8':list(range(34,45)),
'55e9b9ae113f7a2d':list(range(13,17)),
'607848dedc3157d7':list(range(1,8)),
'687a6cc41b1b467d':list(range(1,6)),
'76b40106fea15ebb':list(range(22,30)),
'77219c48a9bfaff5':[1,2],
'7eb11fdf0ed64f2d':list(range(29,36)),
'91f0c5c9c783c128':list(range(1,11)),
'95723042531130d5':[1,2],
'989700773cd625a0':list(range(6,11)),
'9babb9732af227db':list(range(20,25)),
'9ee9faa1cb067728':list(range(1,19)),
'add6d4e3c4f0027a':[18,19,20],
'addb3d02c585ebb3':list(range(83,101)),
'b2b22700aa9f6414':list(range(5,9)),
'c559d1ef651e1996':[1,2],
'cf727cf4e9724481':list(range(30,37)),
'e1379c8287b422e7':list(range(1,9)),
'e37a3a33da818877':[1,2,3],
'e4ae0e1cd09b1f6c':[1,2,3,4,5],
'f53546919a57ada9':list(range(21,28)),
'ff5924209372dc9d':list(range(79,92)),
}
def clean(s):return re.sub(r'\s+',' ',s or '').strip()
def run(item):
 key,pages=item;target=root/(key+'.selected.json')
 if target.exists():return
 doc=fitz.open(root/(key+'.pdf'));out=[]
 for n in pages:
  if n>len(doc):continue
  page=doc[n-1];names=[]
  for tab in page.find_tables().tables:
   for row in tab.extract():
    cells=[clean(x) for x in row]
    candidate=None
    for j,c in enumerate(cells):
     if j and c in ['O','F','W','OzW','OF','O/F','O/W'] and len(cells[j-1])>3:
      candidate=cells[j-1];break
    if candidate is None and cells and re.fullmatch(r'\d+[.]?',cells[0]) and len(cells)>2:
     if any(re.search(r'wykład|konwers|seminar|warsztat|ćwiczen|lektorat|laborat|obowiązkow|fakult|^O$|^F$|^W$',x,re.I) for x in cells[2:]):candidate=cells[1]
    if candidate and not any(t in candidate.lower() for t in ['suma godzin','razem','liczba godzin','nazwa przedmiotu','liczba punkt','seminarium wykład']):names.append(candidate)
  out.append({'page':n,'context':clean(page.get_text()[:180]),'subjects':list(dict.fromkeys(names))})
 target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
 return key,sum(len(g['subjects']) for g in out)
if __name__=='__main__':
 with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
  for result in pool.map(run,configs.items()):print(result,flush=True)
