"""Kontrola źródeł przed siecią — dla ręcznych skryptów researchu."""
import json
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, urlencode, urljoin
import requests

POLICY_PATH=Path(__file__).resolve().parents[1]/'src/data/source-policy.json'
def canonical(url):
    u=urlsplit(url)
    host=(u.hostname or '').lower().removeprefix('www.')
    query=urlencode(sorted((k,v) for k,v in parse_qsl(u.query,keep_blank_values=True) if not k.startswith('utm_') and k not in ['fbclid','gclid']))
    return host,u.path.rstrip('/') or '/',query

def ensure_source_allowed(url,purpose='current'):
    if purpose not in ['current','history']:
        raise ValueError('Nieprawidłowy cel odczytu')
    if urlsplit(url).scheme not in ['http','https']:
        raise ValueError('Adres musi być HTTP/HTTPS')
    candidate=canonical(url)
    policy=json.loads(POLICY_PATH.read_text(encoding='utf-8'))
    for entry in policy['excludedPages']:
        if purpose=='history' and entry['scope']=='current':
            continue
        blocked=canonical(entry['url'])
        match=candidate[0]==blocked[0] and (entry['match']=='host' or entry['match']=='page' and candidate[1:]==blocked[1:] or entry['match']=='prefix' and (candidate[1]==blocked[1] or candidate[1].startswith(blocked[1]+'/')))
        if match:
            raise ValueError('POMIŃ: '+entry['reason'])

def guarded_get(url,purpose='current',timeout=35,headers=None,max_bytes=None):
    # Każde przekierowanie sprawdzamy przed pobraniem jego celu.
    for _ in range(10):
        ensure_source_allowed(url,purpose)
        response=requests.get(url,timeout=timeout,allow_redirects=False,headers=headers,stream=max_bytes is not None)
        if response.status_code in [301,302,303,307,308] and response.headers.get('Location'):
            url=urljoin(url,response.headers['Location'])
            response.close()
            continue
        response.raise_for_status()
        if max_bytes is not None:
            chunks=[]
            size=0
            try:
                for chunk in response.iter_content(chunk_size=65536):
                    size+=len(chunk)
                    if size>max_bytes:
                        raise ValueError('Materiał przekracza limit pobierania')
                    chunks.append(chunk)
                # Zachowujemy zgodny interfejs Response (.content/.text) dla istniejących skryptów.
                response._content=b''.join(chunks)
                response._content_consumed=True
            finally:
                response.close()
        return response
    raise ValueError('Zbyt wiele przekierowań')
