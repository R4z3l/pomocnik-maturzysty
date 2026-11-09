import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { calculateAdmission } from '../src/admission.ts';
import { emptyProfile } from '../src/logic.ts';
import { parseThresholds } from '../src/thresholds.ts';
import type { AdmissionRule, Catalogue } from '../src/types.ts';

const read = (path: string) => JSON.parse(readFileSync(new URL(path, import.meta.url), 'utf8'));
const data: Catalogue = read('../src/data/pwr.json');
const rules: AdmissionRule[] = read('../src/data/pwr-rules.json');

test('Politechnika Wrocławska: pełny zakres Wrocławia, zgodna historia i obliczenia PP/PR 2027/28', () => {
  const audit = read('../docs/research/pwr/audit.json');
  assert.equal(audit.listCount, 64);
  assert.equal(audit.rows.filter((r: { included: boolean }) => !r.included).length, 2);
  assert.equal(data.programmes.length, 62);
  assert.equal(data.programmes.filter(p => p.level === 'long-cycle').length, 1);
  assert.equal(data.programmes.filter(p => p.language === 'en').length, 5);
  assert.ok(data.programmes.every(p => p.city === 'Wrocław' && p.referenceYear === '2026/2027'));
  assert.equal(data.programmes.find(p => p.level === 'long-cycle')?.name, 'Lekarski');
  assert.ok(!data.programmes.some(p => /mikrosystemów|infrastrukturą/.test(p.name)));
  const subjects = read('../docs/research/pwr/additional-subjects-2027.json');
  const symbols: Record<string, string> = { B: 'biologia', Z: 'biznes i zarządzanie', C: 'chemia', F: 'fizyka', G: 'geografia', I: 'informatyka', M: 'matematyka' };
  const review = readFileSync(new URL('../docs/research/pwr/subjects-review.txt', import.meta.url), 'utf8').split('\n').filter(line => line && !line.startsWith('#'));
  assert.equal(Object.keys(subjects).length, review.length);
  for (const line of review) {
    const [name, codes] = line.split('|');
    assert.deepEqual(subjects[name.toLocaleLowerCase('pl')], codes.trim().split(' ').map(code => symbols[code]), name);
  }
  const active = read('../docs/research/pwr/thresholds-active.json');
  const parsed = parseThresholds(active.tables);
  assert.deepEqual(parsed, read('../docs/research/pwr/thresholds-parsed.json'));
  assert.deepEqual(active.tables.map((t: { year: string }) => t.year), ['2026/2027', '2025/2026', '2024/2025']);
  const normalized = (s: string) => s.toLocaleLowerCase('pl').replace('w j. angielskim', 'w języku angielskim');
  for (const programme of data.programmes) {
    const expected = parsed.filter(t => t.inScope && t.status === 'value' && normalized(t.programme) === normalized(programme.name));
    assert.deepEqual(programme.thresholds.map(t => [t.year, t.round, t.value]), expected.map(t => [t.year, t.round, t.value]), programme.id);
  }
  const rule = (name: string) => rules.find(r => r.id === data.programmes.find(p => p.name === name)?.admissionRuleId)!;
  const ordinary = rule('Informatyka algorytmiczna');
  const p = emptyProfile();
  // M = max(80,80+1.5*20,2.5*20)=110; PD=2.5*40=100;
  // JO=0.1*max(90,90+1.5*20,2.5*20)=12; JP=0.1*60=6.
  p.basicScores = { matematyka: 80, 'język angielski': 90, 'język polski': 60 };
  p.subjects = { matematyka: 20, informatyka: 40, 'język angielski': 20 };
  assert.equal(calculateAdmission(ordinary, p).total, 228);
  p.subjects.informatyka = null;
  assert.equal(calculateAdmission(ordinary, p).total, null);
  p.subjects = { matematyka: 0, informatyka: 0 };
  p.basicScores.matematyka = 0;
  assert.equal(calculateAdmission(ordinary, p).total, 0);
  const reuse = emptyProfile();
  reuse.subjects = { matematyka: 80 };
  // Tabela dopuszcza matematykę jako M i PD; to nie są dwa różne przedmioty.
  assert.equal(calculateAdmission(rule('Automatyka i robotyka'), reuse).total, 400);
  const max = emptyProfile();
  max.subjects = Object.fromEntries(['matematyka', 'fizyka', 'chemia', 'biologia', 'informatyka', 'język angielski', 'język polski'].map(s => [s, 100]));
  max.basicScores = { ...max.subjects };
  for (const r of rules) {
    if (r.extraExam) max.admissionExtras = { [r.id]: 660 };
    const result = calculateAdmission(r, max);
    assert.equal(result.status, 'complete', r.id);
    assert.equal(result.total, r.extraExam ? 1195 : r.minimumTotal ? 785 : 535, r.id);
  }
  const arch = rule('Architektura');
  max.admissionExtras = {};
  assert.equal(calculateAdmission(arch, max).total, null);
  max.admissionExtras[arch.id] = 239;
  assert.equal(calculateAdmission(arch, max).status, 'requirement');
  max.admissionExtras[arch.id] = 240;
  assert.equal(calculateAdmission(arch, max).status, 'complete');
  max.admissionExtras[arch.id] = 661;
  assert.throws(() => calculateAdmission(arch, max));
  const med = rule('Lekarski');
  max.subjects.biologia = 0;
  assert.equal(calculateAdmission(med, max).total, 0);
  assert.equal(calculateAdmission(med, max).status, 'requirement');
  const minimum = emptyProfile();
  minimum.subjects = { biologia: 100, matematyka: 100 };
  assert.equal(calculateAdmission(med, minimum).total, 500);
  assert.equal(calculateAdmission(med, minimum).status, 'complete');
  minimum.subjects.biologia = 99;
  assert.equal(calculateAdmission(med, minimum).status, 'requirement');
  minimum.bilingualScores = { 'język angielski': 100 };
  assert.equal(calculateAdmission(med, minimum).total, null);
});
