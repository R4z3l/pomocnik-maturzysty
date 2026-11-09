import json,re,concurrent.futures
from pathlib import Path
from urllib.parse import urlsplit,parse_qs,urlunsplit,urlencode
from bs4 import BeautifulSoup
from source_policy import guarded_get
D=json.loads(Path('src/data/uwr.json').read_text(encoding='utf8'))
rows=D['programmes'][45:]
sources={s['id']:s for s in D['sources']}
out=Path('docs/research/curricula/uwr-b/cache');out.mkdir(parents=True,exist_ok=True)
def fetch(p):
 sid=p['sourceIds'][0]; src=sources[sid]; url=src['url']; u=urlsplit(url); q=dict(parse_qs(u.query)); q['tab']=['program-studies']
 url=urlunsplit((u.scheme,u.netloc,u.path,urlencode(q,doseq=True),''))
 cache=out/(p['id']+'.html')
 if not cache.exists():
  try:
   r=guarded_get(url,'current'); r.encoding='utf8'; cache.write_text(r.text,encoding='utf8')
  except Exception as e:return {'id':p['id'],'name':p['name'],'url':url,'error':str(e)}
 text=cache.read_text(encoding='utf8'); soup=BeautifulSoup(text,'html.parser')
 return {'id':p['id'],'name':p['name'],'url':url,'title':soup.title.get_text(' ',strip=True) if soup.title else '', 'text':soup.get_text(' ',strip=True)[:10000], 'links':[{'text':a.get_text(' ',strip=True),'href':a.get('href')} for a in soup.select('a[href]') if any(x in (a.get_text(' ',strip=True)+' '+a['href']).lower() for x in ['program','plan','pdf','studia'])]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: data=list(ex.map(fetch,rows))
Path('docs/research/curricula/uwr-b/cards.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'total':len(data),'errors':sum('error'in x for x in data),'items':[{k:x.get(k) for k in ['id','title','error']} for x in data]},ensure_ascii=False))
