import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { calculateAdmission } from '../src/admission.ts';
import { extensionFit, matchMatura } from '../src/maturaMatching.ts';
import { emptyProfile } from '../src/logic.ts';
import type { AdmissionRule, Programme } from '../src/types.ts';
const read=(file:string)=>JSON.parse(readFileSync(new URL(`../src/data/${file}.json`,import.meta.url),'utf8'));
const programmes:Programme[]=read('umw').programmes;
const rules:AdmissionRule[]=read('umw-rules');
const rule=(slug:string,year=2027)=>rules.find(r=>r.id===`umw-${slug}-${year}`)!;

test('Uniwersytet Medyczny: zakres, roczniki i oficjalne progi bez filii, II stopnia i English Division',()=>{
 assert.equal(programmes.length,16);assert.equal(programmes.filter(p=>p.language==='en').length,3);
 assert.equal(rules.length,26);assert.equal(programmes.flatMap(p=>p.thresholds).length,35);
 assert.ok(programmes.every(p=>p.city==='Wrocław'&&p.duration&&p.referenceYear==='2026/2027'));
 assert.ok(programmes.filter(p=>p.language==='en').every(p=>!p.admissionRuleId&&!p.thresholds.length));
 assert.ok(programmes.filter(p=>p.language==='pl').every(p=>rules.some(r=>r.id===p.historicalAdmissionRuleId)));
 assert.equal(programmes.find(p=>p.id==='umw-lekarski')!.thresholds[0].value,165);
 assert.ok(programmes.every(p=>!p.name.includes('Optometria')&&!p.name.includes('Wałbrzych')));
});

test('Uniwersytet Medyczny: minima, zaokrąglenie, rozłączne przedmioty i zmiany 2027/28',()=>{
 const p=emptyProfile();p.subjects={biologia:80,chemia:85};
 assert.equal(calculateAdmission(rule('lekarski'),p).total,165);
 assert.equal(matchMatura([programmes.find(p=>p.id==='umw-lekarski')!],rules,p)[0].thresholds[0].delta,0);
 p.subjects={biologia:30,chemia:30};assert.equal(calculateAdmission(rule('lekarski'),p).status,'requirement');
 p.subjects={biologia:null,chemia:90};assert.equal(calculateAdmission(rule('lekarski'),p).total,null);
 p.subjects={biologia:0,chemia:90};assert.equal(calculateAdmission(rule('lekarski'),p).status,'requirement');
 p.subjects={biologia:80,matematyka:90};assert.equal(calculateAdmission(rule('farmacja'),p).total,170);
 assert.equal(calculateAdmission(rule('farmacja',2026),p).total,null);
 p.subjects={};p.basicScores={biologia:49,matematyka:48};
 assert.equal(calculateAdmission(rule('pielegniarstwo'),p).total,77); // round(39.2)+round(38.4)
 p.basicScores={biologia:30,matematyka:30};
 assert.equal(calculateAdmission(rule('pielegniarstwo'),p).total,48); // 2027: minima in percent
 assert.equal(calculateAdmission(rule('pielegniarstwo',2026),p).status,'requirement'); // 2026: minima in points
 p.basicScores={biologia:100};p.subjects={biologia:100};
 assert.notEqual(calculateAdmission(rule('pielegniarstwo'),p).status,'complete'); // PP+PR not two subjects
 assert.equal(extensionFit(rule('pielegniarstwo'),['biologia']).ratio,.5);
 p.subjects={};p.basicScores={'język polski':80,'język angielski':90,matematyka:100};
 assert.equal(calculateAdmission(rule('psychologia'),p).total,189);
 assert.equal(calculateAdmission(rule('psychologia',2026),p).total,216);
 p.subjects={'język polski':80,'język niemiecki':90,biologia:70};p.basicScores={};
 assert.equal(calculateAdmission(rule('psychologia'),p).total,240);
 assert.equal(calculateAdmission(rule('psychologia',2026),p).total,null);
 p.subjects={biologia:70};p.bilingualScores={'język angielski':80};
 assert.equal(calculateAdmission(rule('pielegniarstwo'),p).total,150);
 assert.equal(calculateAdmission(rule('pielegniarstwo',2026),p).total,null);
});
