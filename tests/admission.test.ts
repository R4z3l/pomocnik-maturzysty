import { test } from 'node:test';
import assert from 'node:assert/strict';
import { calculateAdmission, UEW_PL, UEW_EN, UEW_PL_2027, UEW_EN_2027 } from '../src/admission.ts';
import { emptyProfile, parseProfile } from '../src/logic.ts';
import type { AdmissionRule } from '../src/types.ts';
test('wykluczenie przedmiotu wymaga najlepszego wspólnego wariantu, nie wyboru zachłannego',()=>{
 const factors={basic:0,extended:1,bilingual:0};
 const rule:AdmissionRule={...UEW_PL,groups:[{label:'A',subjects:['matematyka','historia'],factors,weight:1},{label:'B',subjects:['matematyka'],factors,weight:1,excludeSubjectsFromGroups:[0],optional:true}]};
 const p=emptyProfile();p.subjects={matematyka:90,historia:80};
 assert.equal(calculateAdmission(rule,p).total,170);
 const mixed:AdmissionRule={...rule,minimumTotal:200,groups:[{...rule.groups[0],options:[{subject:'matematyka',basic:.5,extended:1,bilingual:0},{subject:'historia',basic:0,extended:1,bilingual:0}]}]};
 assert.equal(calculateAdmission(mixed,p).status,'requirement');
});
test('UEW wybiera lepszy poziom każdego przedmiotu i najlepszy przedmiot do wyboru', () => {
  const p = emptyProfile(); p.basicScores = {matematyka: 100, 'język angielski': 80, 'język polski': 90};
  p.subjects = {matematyka: 40, biologia: 75};
  assert.equal(calculateAdmission(UEW_PL,p).total,165);
  p.bilingualScores={'język angielski':80};
  assert.equal(calculateAdmission(UEW_PL,p).total,245);
  p.subjects.biologia=null;
  assert.equal(calculateAdmission(UEW_PL,p).total,null);
});
test('EN nie przyjmuje podstawowego angielskiego ani rozszerzenia poniżej60; zero różne brak', () => {
  const p=emptyProfile(); p.subjects={matematyka:100,'język angielski':59,biologia:100};
  assert.equal(calculateAdmission(UEW_EN,p).status,'requirement');
  p.subjects['język angielski']=60;
  assert.equal(calculateAdmission(UEW_EN,p).total,260);
  p.subjects.matematyka=0;
  assert.equal(calculateAdmission(UEW_EN,p).total,160);
  delete p.subjects.matematyka;
  assert.equal(calculateAdmission(UEW_EN,p).total,null);
});
test('nowe pola profilu zachowują kompatybilność i walidację importu', () => {
  const p=emptyProfile();p.basicScores={matematyka:0};p.careerChoices={test:'finance'};
  p.preferences={tasks:['dane'],mobility:'local',maxStudyYears:3,avoidShifts:true,strictMobility:true};
  assert.deepEqual(parseProfile(JSON.stringify(p)),p);
  assert.throws(()=>parseProfile(JSON.stringify({...p,basicScores:{matematyka:101}})));
});

test('nieobsługiwana matura dwujęzyczna UWr nie jest po cichu pomijana', () => {
  const p=emptyProfile();p.subjects={matematyka:100,'język angielski':80,biologia:100};p.bilingualScores={'język angielski':90};
  const rule={...UEW_PL,id:'uwr-test-2027'};
  const result=calculateAdmission(rule,p);
  assert.equal(result.total,null);
  assert.match(result.rows[0].detail,/dwujęzycz/);
});


test('warunek formalny angielski PP75 lub PR30 działa niezależnie od punktowanej grupy',()=>{
 const rule:AdmissionRule={...UEW_PL,requirements:[{label:'Angielski',options:[{subject:'język angielski',level:'basic',minPercent:75},{subject:'język angielski',level:'extended',minPercent:30}]}]};
 const p=emptyProfile();p.subjects={matematyka:80,'język angielski':29,biologia:80};
 assert.equal(calculateAdmission(rule,p).status,'requirement');
 p.basicScores={'język angielski':75};assert.equal(calculateAdmission(rule,p).status,'complete');
 p.basicScores['język angielski']=74;assert.equal(calculateAdmission(rule,p).status,'requirement');
 p.subjects['język angielski']=30;assert.equal(calculateAdmission(rule,p).status,'complete');
});

test('rozmowa nie jest zerem przy braku; jej punkty nie zastępują minimum matur',()=>{
 const rule:AdmissionRule={...UEW_PL,id:'test-interview',minimumMaturaTotal:240,extraExam:{key:'interview',label:'Rozmowa',min:0,max:440,passMin:264,allowedValues:[0,264,308,352,396,440],note:'Dodatkowy etap'}};
 const p=emptyProfile();p.subjects={matematyka:80,'język angielski':80,biologia:80};
 assert.equal(calculateAdmission(rule,p).total,null);
 p.admissionExtras={[rule.id]:264};assert.equal(calculateAdmission(rule,p).total,504);
 p.subjects.matematyka=79;assert.equal(calculateAdmission(rule,p).status,'requirement');
 p.subjects.matematyka=80;p.admissionExtras[rule.id]=0;assert.equal(calculateAdmission(rule,p).status,'requirement');
 p.admissionExtras[rule.id]=265;assert.throws(()=>calculateAdmission(rule,p));
 assert.deepEqual(parseProfile(JSON.stringify(p)).admissionExtras,p.admissionExtras);
 assert.throws(()=>parseProfile(JSON.stringify({...p,admissionExtras:{test:-1}})));
});


test('rocznik2027 Uniwersytetu Ekonomicznego dodaje biznes, starsze reguły zachowują listę',()=>{
 const p=emptyProfile();p.subjects={matematyka:80,'język angielski':60,'biznes i zarządzanie':100};
 assert.equal(calculateAdmission(UEW_PL,p).total,null);
 assert.equal(calculateAdmission(UEW_PL_2027,p).total,240);
 assert.equal(calculateAdmission(UEW_EN_2027,p).total,240);
 p.subjects['język angielski']=59;assert.equal(calculateAdmission(UEW_EN_2027,p).status,'requirement');
});
