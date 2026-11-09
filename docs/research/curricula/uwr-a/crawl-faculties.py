import sys,subprocess,json,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
sys.path.insert(0,'scripts'); from source_policy import guarded_get
sys.stdout.reconfigure(encoding='utf-8')
D=Path('docs/research/curricula/uwr-a'); jobs={}
for p in D.glob('*-about.html'):
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 for a in s.select('a[href]'):
  u=a['href'].strip()
  if a.get_text(' ',strip=True)=='Sprawdź' and u.startswith('http') and '.uwr.edu.pl' in u:
   jobs.setdefault(u,[]).append(p.stem.removesuffix('-about'));break

def fetch(t):
 u,ids=t; fn='faculty-'+ids[0]+'.html'
 try:
  subprocess.run(['node','--experimental-strip-types','scripts/check-source.ts',u,'current'],check=True,capture_output=True)
  r=guarded_get(u,timeout=25); r.encoding='utf-8'; (D/fn).write_text(r.text,encoding='utf-8');s=BeautifulSoup(r.text,'html.parser')
  links=[(a.get_text(' ',strip=True),a['href']) for a in s.select('a[href]') if any(w in (a.get_text(' ',strip=True)+' '+a['href']).lower() for w in ['program','plan','sylabus','stopnia','kierunki']) and 'wp-login' not in a['href'] and 'dostep-multiportal' not in a['href']]
  return {'url':u,'ids':ids,'file':fn,'links':list(dict.fromkeys(links))}
 except Exception as e:return {'url':u,'ids':ids,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(fetch,jobs.items()))
(D/'faculty-links.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
for r in rows: print(r['ids'],r.get('error',r.get('links')))
