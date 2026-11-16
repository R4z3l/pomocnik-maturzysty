import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { calculateAdmission } from '../src/admission.ts';
import { emptyProfile } from '../src/logic.ts';
import { suggestedFamilies } from '../src/careers.ts';
import type { AdmissionRule, Programme } from '../src/types.ts';
const read = (name: string) => JSON.parse(readFileSync(new URL(`../src/data/${name}.json`, import.meta.url), 'utf8'));
const rules: AdmissionRule[] = read('upwr-rules');
const programmes: Programme[] = read('upwr').programmes;
const rule = (id: string) => rules.find(r => r.id === `upwr-${id}-2027`)!;

test('Uniwersytet Przyrodniczy we Wrocławiu: pełny spis, osobne języki i roczniki', () => {
  assert.equal(programmes.length, 28);
  assert.equal(programmes.filter(p => p.language === 'en').length, 2);
  assert.equal(programmes.filter(p => p.level === 'long-cycle').length, 2);
  assert.ok(programmes.every(p => p.duration && p.referenceYear === '2026/2027' && rules.some(r => r.id === p.admissionRuleId && r.year === '2027/2028')));
  assert.equal(new Set(programmes.map(p => p.id)).size, 28);
});

test('Uniwersytet Przyrodniczy we Wrocławiu: PP/PR, wybór przedmiotu, zero i brak', () => {
  const p = emptyProfile();
  p.basicScores = { 'język polski': 80, 'język angielski': 90, matematyka: 100, biologia: 100 };
  p.subjects = { 'język polski': 50, 'język angielski': 30, biologia: 70, chemia: 65 };
  // max(32,50) + max(36,30) + 10*70 = 786; biologia PP jest pomijana.
  assert.equal(calculateAdmission(rule('biologia'), p).total, 786);
  p.subjects = {};assert.equal(calculateAdmission(rule('biologia'), p).total, 468);
  p.subjects = {biologia:null};assert.equal(calculateAdmission(rule('biologia'), p).total, null);
  p.subjects = {biologia:0};assert.equal(calculateAdmission(rule('biologia'), p).total, 468);
  p.bilingualScores = {'język angielski':90};assert.equal(calculateAdmission(rule('biologia'), p).status, 'missing');
});

test('Uniwersytet Przyrodniczy we Wrocławiu: matematyka PP w osobnej grupie technicznej', () => {
  const p = emptyProfile();p.basicScores = {'język polski':80,'język angielski':90,matematyka:100};p.subjects={matematyka:70,fizyka:60,geografia:100};
  assert.equal(calculateAdmission(rule('budownictwo'),p).total, 1168); // 32+36+400+700; geografia nie jest dopuszczona.
  assert.equal(calculateAdmission(rule('geodezja-i-kartografia'),p).total, 1468); // geografia PR dopuszczona.
});

test('Weterynaria: minima obu przedmiotów, matematyka tylko w polskim wariancie', () => {
  const p=emptyProfile();p.subjects={biologia:29,chemia:90,matematyka:100};
  assert.equal(calculateAdmission(rule('weterynaria'),p).status,'requirement');
  p.subjects={biologia:30,chemia:0,matematyka:40};assert.equal(calculateAdmission(rule('weterynaria'),p).total,70);
  p.subjects={biologia:30,chemia:30};const en=rule('weterynaria-w-jezyku-angielskim');
  assert.equal(calculateAdmission(en,p).total,null); // brak potwierdzenia zwolnienia/B2.
  p.admissionExtras={[en.id]:100};assert.equal(calculateAdmission(en,p).total,160);
  p.subjects={biologia:30,matematyka:100};assert.equal(calculateAdmission(en,p).total,null);
});

test('Uniwersytet Przyrodniczy we Wrocławiu: portale nie stają się oficjalnymi progami ani zerami', () => {
  const history=programmes.flatMap(p=>p.thresholds);
  assert.equal(history.length,53);
  assert.equal(history.filter(t=>t.year==='2026/2027').length,27);
  assert.equal(history.filter(t=>t.year==='2025/2026').length,26);
  assert.ok(history.every(t=>t.status==='reported'&&t.basis==='unspecified'&&t.round===null&&t.value>0));
  assert.equal(programmes.find(p=>p.id==='upwr-weterynaria-w-jezyku-angielskim')!.thresholds.length,0);
  assert.equal(programmes.find(p=>p.id==='upwr-weterynaria')!.thresholds.find(t=>t.year==='2026/2027')!.value,126);
});

test('Język prowadzenia weterynarii nie oznacza ścieżki filologicznej', () => {
  for(const p of programmes.filter(p=>p.level==='long-cycle'))assert.deepEqual(suggestedFamilies(p),[]);
});
