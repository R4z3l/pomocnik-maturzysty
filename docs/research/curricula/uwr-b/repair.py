"""Re-extract course-name cells, never a whole strip containing module columns.
Page ranges were checked against degree/mode headings in the cached documents.
No network access.
"""
import json,re,runpy
from pathlib import Path
import pymupdf as fitz
ROOT=Path(__file__).parent
CACHE=ROOT/'cache'
configs=runpy.run_path(str(ROOT/'extract.py'))['configs']
configs.update({'56931a4e3c053d65':range(1,8),'0a82482251f76c17':range(44,78),'2b5b748ee09d20ad':range(28,33),'7eb11fdf0ed64f2d':range(31,36),'8aa125798454591a':range(2,18),'b87f7dfefa066a85':range(3,9),'989700773cd625a0':range(3,10),'b2b22700aa9f6414':range(2,9)})
STATUS={'O','F','W','OzW','OF','O/F','O/W','Obowiązkowy','Wybieralny'}
def clean(s):
 s=re.sub(r'(\w)-\s*\n\s*(\w)',r'\1\2',s)
 s=re.sub(r'\s+',' ',s).strip().replace('\xad','')
 return s

def cell_text(page,box):
 rect=fitz.Rect(box)
 if page.rotation:return clean(page.get_text(clip=rect*page.derotation_matrix))
 words=[w for w in page.get_text('words') if rect.x0-.5<=(w[0]+w[2])/2<=rect.x1+.5 and rect.y0-.5<=(w[1]+w[3])/2<=rect.y1+.5]
 words.sort(key=lambda w:(round(w[1]/3),w[0]))
 return clean(' '.join(w[4] for w in words))

def extract(key,pages):
 doc=fitz.open(CACHE/(key+'.pdf'));groups=[]
 for n in pages:
  if n>len(doc):continue
  page=doc[n-1];names=[]
  for table in page.find_tables().tables:
   rows=table.extract()
   for row,geom in zip(rows,table.rows):
    cells=[clean(c or '') for c in row]
    status=next((i for i,c in enumerate(cells) if c in STATUS and i>0),None)
    if status is None:continue
    preceding=[j for j in range(status) if cells[j] and geom.cells[j]]
    if not preceding:continue
    j=preceding[-1]
    name=cell_text(page,geom.cells[j])
    name=re.sub(r'\(\d+ ECTS\)','',name).strip()
    # Repeated headers, legend and module totals never represent courses.
    if re.fullmatch(r'(?:Łącznie|Razem|Suma|Total)[:.]?',name,re.I):continue
    if len(name)<4 or re.search(r'RAZEM|SUMA|Nazwa przedmiotu|Przedmiot:|obowiązkowy z|Cele kształcenia|^ECTS$|należy wybrać',name,re.I):continue
    if re.fullmatch(r'[0-9. ]+',name):continue
    names.append(name)
  groups.append({'page':n,'context':clean(page.get_text()[:180]),'subjects':list(dict.fromkeys(names))})
 (CACHE/(key+'.repaired.json')).write_text(json.dumps(groups,ensure_ascii=False,indent=2),encoding='utf8')
 print(key,sum(len(g['subjects']) for g in groups),flush=True)
 return groups
if __name__=='__main__':
 import concurrent.futures
 with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
  jobs=[pool.submit(extract,key,pages) for key,pages in configs.items() if (CACHE/(key+'.pdf')).exists() and not (CACHE/(key+'.repaired.json')).exists()]
  for job in jobs:job.result()
