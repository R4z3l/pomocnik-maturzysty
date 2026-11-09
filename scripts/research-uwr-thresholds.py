"""Ręczny research publicznych stron, poza aplikacją. Wymaga requests i bs4."""
import concurrent.futures
import json
import re
from pathlib import Path
from urllib.parse import urljoin
from source_policy import guarded_get
from bs4 import BeautifulSoup

BASE = 'https://dostanesie.pl'
CHECKED = '2026-10-25'
HISTORY_YEARS=set(json.loads(Path('src/data/source-policy.json').read_text(encoding='utf-8'))['history']['admissionYears'])

def soup(url):
    r = guarded_get(url, purpose='history', timeout=35)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'html.parser')

def fetch(item):
    name, url = item
    try:
        page = soup(url)
        rows = []
        for table in page.select('table'):
            headers = [c.get_text(' ',strip=True) for c in table.select('tr')[0].select('th,td')]
            if headers[:2] != ['Rok','Tura']:
                continue
            for tr in table.select('tr')[1:]:
                cells = [c.get_text(' ',strip=True) for c in tr.select('td')]
                if len(cells)<3 or not re.fullmatch(r'20[0-9]{2}',cells[0]):
                    continue
                year = int(cells[0])
                if year not in HISTORY_YEARS:
                    continue
                match=re.fullmatch(r'([0-9]+(?:[.,][0-9]+)?)\s*pkt',cells[2])
                if match:
                    rows.append({'year':f'{year}/{year+1}','round':cells[1] or None,'value':float(match[1].replace(',','.')),'raw':cells[:3]})
        # Metadata retained to spot wrong level / language / modes in the portal.
        text=page.get_text(' ',strip=True)
        start=text.find('Wydział')
        metadata=text[start:start+500]
        return {'name':name,'url':url,'checkedAt':CHECKED,'rows':rows,'metadata':metadata,'error':None}
    except Exception as e:
        return {'name':name,'url':url,'checkedAt':CHECKED,'rows':[],'error':str(e)}

if __name__ == '__main__':
    listing=soup(BASE+'/uczelnia/uwr')
    links={a.get_text(' ',strip=True):urljoin(BASE,a['href']) for a in listing.select('table a')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        records=list(pool.map(fetch,links.items()))
    output={'checkedAt':CHECKED,'listingUrl':BASE+'/uczelnia/uwr','records':records}
    Path('docs/research/uwr-thresholds-dostanesie.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'pages':len(records),'rows':sum(len(r['rows']) for r in records),'errors':sum(bool(r['error']) for r in records)}))
