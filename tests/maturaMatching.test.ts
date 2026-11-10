import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { extensionFit, matchMatura } from '../src/maturaMatching.ts';
import { UEW_PL_2027 } from '../src/admission.ts';
import { emptyProfile } from '../src/logic.ts';
import type { AdmissionRule, Programme } from '../src/types.ts';
const read = (name: string) => JSON.parse(readFileSync(new URL(`../src/data/${name}.json`, import.meta.url), 'utf8'));

test('Dopasowanie matury: wagi, alternatywy, odrębne roczniki, braki i cały katalog', () => {
  const weighted: AdmissionRule = { ...UEW_PL_2027, groups: [
    { label: 'Główny', subjects: ['biologia','chemia'], factors: { basic: 0, extended: 1, bilingual: 0 }, weight: 10 },
    { label: 'Język', subjects: ['język angielski'], factors: { basic: 0, extended: 1, bilingual: 0 }, weight: 1 },
  ] };
  assert.equal(extensionFit(weighted, ['biologia']).ratio, 10/11);
  assert.equal(extensionFit(weighted, ['język angielski']).ratio, 1/11);
  assert.equal(extensionFit(weighted, ['biologia','chemia']).ratio, 10/11); // alternative, not two bonuses
  assert.deepEqual(extensionFit(weighted, ['biologia','chemia']).rewarded, ['biologia','chemia']);
  assert.equal(extensionFit(weighted, []).ratio, 0);
  const programmes: Programme[] = ['uwr','uew','pwr','upwr'].flatMap(u => read(u).programmes).map(p => p.universityId === 'uew' ? { ...p, admissionRuleId: p.language === 'pl' ? 'uew-2027-pl' : 'uew-2027-en' } : p);
  const rules: AdmissionRule[] = [UEW_PL_2027, ...['uwr','pwr','upwr'].flatMap(u => read(`${u}-rules`))];
  const p = emptyProfile();
  p.subjects = { matematyka: 100, 'język angielski': 100, biologia: 100, 'biznes i zarządzanie': 100 };
  const results = matchMatura(programmes, rules, p);
  assert.equal(results.length, 199);
  assert.ok(results.every(r => !r.fit || r.fit.ratio >= 0 && r.fit.ratio <= 1.000001));
  assert.ok(results.filter(r => r.programme.universityId !== 'uew').every(r => r.thresholds.every(t => t.delta === null) && !r.reachesThreshold));
  const uew = results.find(r => r.programme.universityId === 'uew' && r.programme.language === 'pl')!;
  assert.equal(uew.score?.total, 300);
  assert.equal(uew.historicalScore?.total, 300);
  assert.ok(uew.reachesThreshold);
  const onlyNew = { ...p, subjects: { matematyka: 100, 'język angielski': 100, 'biznes i zarządzanie': 100 } };
  const changed = matchMatura([uew.programme], rules, onlyNew)[0];
  assert.equal(changed.score?.total, 300);
  assert.equal(changed.historicalScore?.total, null); // 2026 did not award business
  assert.equal(changed.reachesThreshold, false);
  p.subjects.biologia = null;
  assert.equal(matchMatura([uew.programme], rules, p)[0].reachesThreshold, false);
  p.subjects = { matematyka: 0, 'język angielski': 0, biologia: 0 };
  assert.equal(matchMatura([uew.programme], rules, p)[0].score?.total, 0);
});
