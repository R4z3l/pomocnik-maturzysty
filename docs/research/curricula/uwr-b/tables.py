from pathlib import Path
import json,sys,concurrent.futures
import pymupdf as fitz
root=Path(__file__).parent/'cache'
def run(p):
 target=p.with_suffix('.tables.json')
 if target.exists():return
 doc=fitz.open(p);out=[]
 for page in doc:
  txt=page.get_text()
  # The appendix has many learning-outcome tables, which are not course lists.
  if len(doc)>12 and not any(t in txt.lower() for t in ['przedmiot','semestr','course','programow']):continue
  for table in page.find_tables().tables:
   out.append({'page':page.number+1,'context':txt[:180],'rows':table.extract()})
 target.write_text(json.dumps(out,ensure_ascii=False),encoding='utf8')
 print(p.name,len(out),flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(run,root.glob('*.pdf')))
