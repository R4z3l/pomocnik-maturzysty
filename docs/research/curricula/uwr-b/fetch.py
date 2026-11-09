import sys,json,hashlib,concurrent.futures
from pathlib import Path
from urllib.parse import urljoin
sys.path.insert(0,str(Path.cwd()/'scripts'))
from source_policy import guarded_get
from bs4 import BeautifulSoup
base=Path('docs/research/curricula/uwr-b/cache')
def fetch(url):
    key=hashlib.sha256(url.encode()).hexdigest()[:16]
    path=base/(key+'.json')
    if path.exists(): return json.loads(path.read_text(encoding='utf-8'))
    try:
        r=guarded_get(url,timeout=22)
        if 'pdf' in r.headers.get('Content-Type','').lower() or r.content[:4]==b'%PDF':
            import fitz
            text='\n'.join(p.get_text() for p in fitz.open(stream=r.content,filetype='pdf'))
            (base/(key+'.pdf')).write_bytes(r.content)
            result={'url':url,'text':text,'links':[]}
        else:
            s=BeautifulSoup(r.content,'html.parser')
            for n in s(['script','style']):n.decompose()
            result={'url':url,'text':s.get_text(' ',strip=True),'links':[{'text':a.get_text(' ',strip=True),'url':urljoin(r.url,a['href'])} for a in s.select('a[href]')]}
        path.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
        return result
    except Exception as e:return {'url':url,'error':str(e)}
if __name__=='__main__':
    urls=sys.argv[1:]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for x in pool.map(fetch,urls):
            print(json.dumps({'url':x['url'],'error':x.get('error'),'length':len(x.get('text','')),'links':[a for a in x.get('links',[]) if any(t in (a['text']+' '+a['url']).lower() for t in ['program','plan','2025','2026'])]},ensure_ascii=False))
