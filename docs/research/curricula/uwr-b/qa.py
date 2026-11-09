import json,re,hashlib
from pathlib import Path
root=Path(__file__).parent
p=Path('src/data/curricula-uwr-b.json');data=json.loads(p.read_text(encoding='utf8'))
expected={x['id'] for x in json.loads(Path('src/data/uwr.json').read_text(encoding='utf8'))['programmes'][45:]}
assert {r['programmeId'] for r in data}==expected
bad=[]
for r in data:
 for g in r['groups']:
  assert g['sourceUrl'] in {s['url'] for s in r['sources']}
  for name in g['subjects']:
   if re.fullmatch(r'(?:Łącznie|Razem|Suma|Total)[:.]?',name,re.I) or re.search(r'Przedmiot:|Cele kształcenia|^ECTS$|^Liczba egzaminów|^O/W/|opcyjne obejmują|[ĞĊĔá]|^[(]PDW-',name):bad.append((r['programmeId'],name))
assert not bad,bad
counts={'records':len(data),'withSubjects':sum(bool(r['groups']) for r in data),'fullPlans':sum(r['completeness']=='full-plan' for r in data),'withSpecializations':sum(bool(r['specializations']) for r in data),'specializationEntries':sum(len(r['specializations']) for r in data),'subjectEntries':sum(len(g['subjects']) for r in data for g in r['groups']),'unavailable':[r['programmeId'] for r in data if not r['groups']],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(root/'qa-summary.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
lines=[]
for r in data:
 lines.extend(['# '+r['programmeId'],r['referenceYear'],r['note']])
 for g in r['groups']:lines.extend(['## '+g['title'],g['sourceUrl']]+['- '+s for s in g['subjects']])
(root/'reviewed-inventory.md').write_text('\n\n'.join(lines)+'\n',encoding='utf8')
print(json.dumps(counts,ensure_ascii=False))
