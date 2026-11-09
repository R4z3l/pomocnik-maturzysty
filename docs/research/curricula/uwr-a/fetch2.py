exec(open('docs/research/curricula/uwr-a/fetch.py',encoding='utf-8-sig').read().split('for name,url')[0])
for name,url in [('bio-plans','https://biologia.uwr.edu.pl/organizacja-roku-akademickiego/plany-zajec/'),('chem-plans','https://chem.uwr.edu.pl/studenci/programy-studiow/'),('roman','https://ifr.uwr.edu.pl/przedmioty-do-wyboru/')]:
 try:
  subprocess.run(['node','--experimental-strip-types','scripts/check-source.ts',url,'current'],check=True,capture_output=True)
  r=guarded_get(url); r.encoding='utf-8'; Path('docs/research/curricula/uwr-a/'+name+'.html').write_text(r.text,encoding='utf-8'); s=BeautifulSoup(r.text,'html.parser')
  print(name,[(a.get_text(' ',strip=True),a.get('href')) for a in s.select('a[href]') if any(w in (a.get_text(' ',strip=True)+' '+a.get('href','')).lower() for w in ['program','plan','stop','2025','2026','wybor'])][-100:])
 except Exception as e: print(name,str(e))
