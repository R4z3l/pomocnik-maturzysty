import json,re
from pathlib import Path
import pymupdf as fitz
from repair import cell_text,clean,CACHE
# Validated columns of the actual official plan, not outcomes or degree-II text.
configs={'684754e44a146247':(range(1,8),0),'95723042531130d5':([1,2],0),'c559d1ef651e1996':([1,2],0),'0a5d70ef73d1329b':(range(1,6),1),'3dbd917e9ca61b20':(range(1,6),1),'28a9217b670ca104':(range(18,21),1),'04781d78c4e3569e':([16],1),'e1379c8287b422e7':(range(1,5),1),'47dd0092d2e5fbd1':(range(1,8),1),'687a6cc41b1b467d':(range(1,5),1)}
def run(key,config):
 pages,col=config;doc=fitz.open(CACHE/(key+'.pdf'));out=[]
 for n in pages:
  if n>len(doc):continue
  page=doc[n-1];names=[]
  if key=='e1379c8287b422e7':
   lines=page.get_text().splitlines()
   translation=str.maketrans({'á':'ł','Ğ':'ś','Ċ':'ę','Ĕ':'ń','Ī':'ż','û':'ć','à':'Ł','ē':'Ń','ĉ':'Ę','ü':'ć','Ĩ':'ź'})
   for i,line in enumerate(lines[:-2]):
    if not re.fullmatch(r'\d{1,2}',line.strip()) or not re.match('[A-ZĄĆĘŁŃÓŚŹŻ]',lines[i+1].strip()):continue
    parts=[]
    for value in lines[i+1:i+9]:
     if re.match(r'^(?:EX|ST|0,|O,)',value.strip()) or re.fullmatch(r'\d+[,\d]*',value.strip()):break
     parts.append(value.strip())
    name=clean(' '.join(parts)).translate(translation)
    if name.startswith(('SEMESTR','RAZEM')):continue
    if name.startswith('Przemiany struktur'):name='Przemiany struktur współczesnego państwa z elementami socjologii administracji'
    if 5<len(name)<180:names.append(name)
   out.append({'page':n,'context':clean(page.get_text()[:180]),'subjects':list(dict.fromkeys(names))});continue
  for table in page.find_tables().tables:
   for row,geom in zip(table.extract(),table.rows):
    if col==1:
     choices=[j for j,c in enumerate(row[1:],1) if c and re.search(r'[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]',c)]
     if not choices:continue
     namecol=choices[0]
    else:namecol=col
    if len(row)<=col or not row[namecol] or not geom.cells[namecol]:continue
    if key=='04781d78c4e3569e' and not (row[0] or '').strip() in ['I','II','III','IV']:continue
    if key in ['28a9217b670ca104','e1379c8287b422e7','0a5d70ef73d1329b','47dd0092d2e5fbd1','687a6cc41b1b467d'] and not re.fullmatch(r'\d+\s*\.?',row[0] or ''):continue
    if key=='3dbd917e9ca61b20' and not (re.fullmatch(r'\d+\s*\.?',row[0] or '') or re.match(r'^[A-D]\.',row[namecol])):continue
    if col==0 and not any(re.fullmatch(r'\d+(?:[.,]\d+)?',str(c or '').strip()) for c in row[1:]):continue
    name=cell_text(page,geom.cells[namecol]);
    if re.fullmatch(r'(?:Łącznie|Razem|Suma|Total)[:.]?',name,re.I):continue
    if len(name)>3 and not re.search(r'Nazwa przedmiotu|SUMA|RAZEM|SEMESTR|ROK STUDI|STACJONARNE|Forma zajęć',name,re.I):names.append(name)
  out.append({'page':n,'context':clean(page.get_text()[:180]),'subjects':list(dict.fromkeys(names))})
 (CACHE/(key+'.repaired.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8');print(key,sum(len(g['subjects']) for g in out),flush=True)
if __name__=='__main__':
 import concurrent.futures
 with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
  jobs=[pool.submit(run,k,v) for k,v in configs.items()]
  for j in jobs:j.result()
