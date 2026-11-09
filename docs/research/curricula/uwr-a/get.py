import sys,json,subprocess,concurrent.futures,re
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0,'scripts');from source_policy import guarded_get
sys.stdout.reconfigure(encoding='utf-8');D=Path('docs/research/curricula/uwr-a')
def fetch(job):
 name,u=job
 try:
  subprocess.run(['node','--experimental-strip-types','scripts/check-source.ts',u,'current'],check=True,capture_output=True)
  r=guarded_get(u,timeout=30)
  if 'pdf' in r.headers.get('content-type','') or u.lower().endswith('.pdf'):
   (D/(name+'.pdf')).write_bytes(r.content)
   import pymupdf
   doc=pymupdf.open(stream=r.content,filetype='pdf');txt='\n'.join(p.get_text(sort=True) for p in doc);(D/(name+'.txt')).write_text(txt,encoding='utf-8');return {'name':name,'url':u,'type':'pdf','chars':len(txt)}
  r.encoding='utf-8';(D/(name+'.html')).write_text(r.text,encoding='utf-8');s=BeautifulSoup(r.text,'html.parser');m=s.select_one('main') or s
  (D/(name+'.txt')).write_text(m.get_text('\n',strip=True),encoding='utf-8')
  links=list(dict.fromkeys((a.get_text(' ',strip=True),a['href']) for a in m.select('a[href]') if 'wp-login' not in a['href']));return {'name':name,'url':u,'type':'html','links':links}
 except Exception as e:return {'name':name,'url':u,'error':str(e)}
if __name__=='__main__':
 jobs=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8-sig'))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(fetch,jobs))
 (D/(Path(sys.argv[1]).stem+'-results.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
 for r in rows:print(r)
