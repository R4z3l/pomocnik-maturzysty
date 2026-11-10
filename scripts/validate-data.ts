import { curricula, validateCurricula } from '../src/curricula.ts';
import { graduateData, validateGraduateData } from '../src/graduates.ts';
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';

import { SUBJECTS } from '../src/types.ts';
import type { AdmissionRule } from '../src/types.ts';
import { UEW_PL, UEW_EN, UEW_PL_2027, UEW_EN_2027, calculateAdmission } from '../src/admission.ts';
import { emptyProfile } from '../src/logic.ts';
import { sourceExclusion, claimRejection, sourcePolicy } from '../src/sources.ts';
import type { Catalogue } from '../src/types.ts';

const read = (name: string) => JSON.parse(readFileSync(new URL('../src/data/' + name + '.json', import.meta.url), 'utf8'));
const uwr = read('uwr'), uew = read('uew'), pwr = read('pwr'), upwr = read('upwr');
const data: Catalogue = {...uwr, universities: [...uwr.universities,...uew.universities,...pwr.universities,...upwr.universities], sources: [...uwr.sources,...uew.sources,...pwr.sources,...upwr.sources], programmes: [...uwr.programmes,...uew.programmes,...pwr.programmes,...upwr.programmes]};
const unique = (ids: string[]) => assert.equal(new Set(ids).size, ids.length, 'Duplikaty identyfikatorów');
unique(data.universities.map(u=>u.id)); unique(data.programmes.map(p=>p.id)); unique(data.sources.map(s=>s.id));
const sourceIds = new Set(data.sources.map(s=>s.id));
const universities = new Set(data.universities.map(u=>u.id));
for (const s of data.sources) {
  assert.equal(new URL(s.url).protocol, 'https:');
  assert.match(s.checkedAt, /^\d{4}-\d{2}-\d{2}$/);
  assert.ok(s.note && s.publisher && s.title);
}
for (const u of data.universities) {
  assert.ok(u.sourceIds.length && u.sourceIds.every(id=>sourceIds.has(id)));
}
for (const p of data.programmes) {
  assert.ok(universities.has(p.universityId), p.id);
  assert.equal(p.city, 'Wrocław', p.id);
  assert.ok(['pl','en'].includes(p.language));
  assert.ok(['bachelor','long-cycle'].includes(p.level));
  assert.ok(p.name && p.description && p.referenceYear && p.admissionNote);
  assert.ok(p.sourceIds.length && p.sourceIds.every(id=>sourceIds.has(id)), p.id);
  assert.ok(p.subjects.every(s=>SUBJECTS.includes(s as typeof SUBJECTS[number])), p.id);
  if (!p.subjectsVerified) assert.equal(p.subjects.length, 0, p.id);
  for (const t of p.thresholds) {
    assert.ok(sourceIds.has(t.sourceId));
    for(const id of [t.sourceId,...(t.supportingSourceIds??[])]){
      const source=data.sources.find(s=>s.id===id);assert.ok(source,p.id);
      assert.equal(sourceExclusion(source.url,'history'),undefined,p.id+' — wykluczone źródło historii');
      assert.equal(claimRejection(source.url,p.id,t.year),undefined,p.id+' — odrzucona informacja');
    }
    assert.ok(Number.isFinite(t.value) && t.value >= 0);
    assert.ok(sourcePolicy.history.admissionYears.some(year=>t.year===`${year}/${year+1}`),'Rocznik poza zakresem aktywnej historii: '+t.year);
    assert.ok(['official','reported','anecdote'].includes(t.status));
    assert.ok(!t.basis||['qualification','admission','unspecified'].includes(t.basis));
  }
}
const uwrRules:AdmissionRule[] = read('uwr-rules');
const rules:AdmissionRule[] = [...read('upwr-rules'), ...read('pwr-rules'), ...uwrRules, UEW_PL, UEW_EN, UEW_PL_2027, UEW_EN_2027];
unique(rules.map((r: {id:string})=>r.id));
for (const r of rules) {
  assert.equal(new URL(r.sourceUrl).protocol, 'https:');
  assert.ok(r.groups.length);
  if(r.extraExam){const e=r.extraExam;assert.ok(e.min>=0&&e.min<=e.passMin&&e.passMin<=e.max,r.id);assert.ok(!e.allowedValues||e.allowedValues.every(v=>v>=e.min&&v<=e.max),r.id);}
  for(const req of r.requirements??[]){assert.ok(req.options.length,r.id);for(const o of req.options){assert.ok(SUBJECTS.includes(o.subject as typeof SUBJECTS[number]),r.id);assert.ok(o.minPercent>=0&&o.minPercent<=100,r.id);}}
  const maxProfile=emptyProfile();maxProfile.subjects=Object.fromEntries(SUBJECTS.map(s=>[s,100]));maxProfile.basicScores={...maxProfile.subjects};
  if(r.extraExam)maxProfile.admissionExtras={[r.id]:r.extraExam.max};
  const maxResult=calculateAdmission(r,maxProfile);assert.equal(maxResult.status,'complete',r.id);assert.ok(Number.isFinite(maxResult.total),r.id);
  for (const [i,g] of r.groups.entries()) {
    assert.ok(g.subjects.every((s:string)=>SUBJECTS.includes(s as typeof SUBJECTS[number])),r.id);
    for(const option of g.options ?? []) {
      assert.ok(g.subjects.includes(option.subject),r.id);
      for(const level of ['basic','extended','bilingual'])assert.ok(Number.isFinite(option[level])&&option[level]>=0,r.id);
    }
    assert.ok((g.excludeSubjectsFromGroups??[]).every((n:number)=>Number.isInteger(n)&&n>=0&&n<i),r.id);
  }
}
for(const p of data.programmes)if(p.admissionRuleId)assert.ok(rules.some((r:{id:string})=>r.id===p.admissionRuleId),p.id);
const jobs=read('jobs'); unique(jobs.jobs.map((j:{id:string})=>j.id)); unique(jobs.jobs.map((j:{url:string})=>j.url));
for(const j of jobs.jobs) {
  assert.ok(jobs.sources.some((s:{id:string})=>s.id===j.sourceId),j.id);
  assert.equal(new URL(j.url).protocol,'https:');
  assert.ok(['confirmed','unconfirmed','expired'].includes(j.active),j.id);
  assert.ok(j.checkedAt<=jobs.checkedAt,j.id);
  if(j.active==='confirmed'&&j.expiresAt)assert.ok(j.expiresAt>=j.checkedAt,j.id);
}
assert.equal(data.universities.length,4); assert.equal(data.programmes.length,199);
console.log(JSON.stringify({universities:data.universities.length,programmes:data.programmes.length,english:data.programmes.filter(p=>p.language==='en').length,sources:data.sources.length,thresholds:data.programmes.reduce((n,p)=>n+p.thresholds.length,0),uwrRules:uwrRules.length,jobs:jobs.jobs.length},null,2));
console.log('OK: wszystkie rekordy bieżącego zakresu czterech uczelni, reguły i próbka ogłoszeń zwalidowane.');

assert.deepEqual(validateGraduateData(graduateData, data.programmes), []);
console.log(`ELA: ${graduateData.matches.length} ofert, ${graduateData.cohorts.length} kohort; walidacja poprawna.`);

assert.deepEqual(validateCurricula(curricula, data.programmes), []);
console.log(`Programy: ${curricula.length} ofert, ${curricula.filter(r=>r.groups.some(g=>g.subjects.length)).length} ze spisem, ${curricula.filter(r=>r.completeness==='full-plan').length} pełnych planów.`);
