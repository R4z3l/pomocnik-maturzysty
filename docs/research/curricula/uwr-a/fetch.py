import sys,subprocess
from pathlib import Path
sys.path.insert(0,'scripts')
from source_policy import guarded_get
from bs4 import BeautifulSoup
for name,url in [('bio','https://biologia.uwr.edu.pl/studiuj-z-nami/'),('chem','https://chem.uwr.edu.pl/studenci/plany-zajec/')]:
 subprocess.run(['node','--experimental-strip-types','scripts/check-source.ts',url,'current'],check=True,capture_output=True)
 r=guarded_get(url); Path('docs/research/curricula/uwr-a/'+name+'.html').write_text(r.text,encoding='utf-8'); s=BeautifulSoup(r.text,'html.parser')
 print(name,[(a.get_text(' ',strip=True),a.get('href')) for a in s.select('a[href]') if any(w in (a.get_text(' ',strip=True)+' '+a.get('href','')).lower() for w in ['program','plan','biologia','chemistry'])][-80:])
