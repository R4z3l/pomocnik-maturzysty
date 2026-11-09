import { test } from 'node:test';
import assert from 'node:assert/strict';
import { emptyProfile, parseProfile, serializeProfile, matrixScore, matchSubjects, filterProgrammes } from '../src/logic.ts';
import type { Programme } from '../src/types.ts';

test('profil zachowuje zero i brak wyniku, odrzuca uszkodzony import bez zmiany oryginału', () => {
  const profile = emptyProfile();
  profile.subjects = { matematyka: 0, biologia: null };
  profile.notes = { oferta: 'Własny wniosek: żółć' };
  assert.deepEqual(parseProfile(JSON.stringify(profile)), profile);
  for (const bad of [null, {}, {...profile, version: 2}, {...profile, subjects: { matematyka: 101 }}, {...profile, subjects: { biologia: -1 }}, {...profile, weights: [1]}, {...profile, weights: [1,1,1,1,1,6]}, {...profile, ratings: { id: [1,2,3,4,5,0] }}, {...profile, comparison: ['a','b','c','d','e']}, {...profile, comparison: ['a','a']}, {...profile, notes: {a: 42}}, {...profile, interests: false}]) {
    assert.throws(() => parseProfile(JSON.stringify(bad)));
  }
  assert.throws(() => parseProfile('{broken'));
  assert.equal(profile.subjects.matematyka, 0);
});

test('zapis i eksport nie tworzą profilu niemożliwego do ponownego odczytu', () => {
  const p = emptyProfile();
  assert.deepEqual(parseProfile(serializeProfile(p)), p);
  p.interests = 'x'.repeat(10001);
  assert.throws(() => serializeProfile(p));
  p.interests = '';
  p.notes.a = 'x'.repeat(20001);
  assert.throws(() => serializeProfile(p));
});

test('macierz nie karze braków zerem ani nie przenosi ich wag na znane kryteria', () => {
  assert.deepEqual(matrixScore([1,1], [5,null]), { min: 3, max: 5, coverage: 0.5, disabled: false });
  assert.deepEqual(matrixScore([1,3], [1,5]), { min: 4, max: 4, coverage: 1, disabled: false });
  assert.deepEqual(matrixScore([0,0], [5,5]), { min: 0, max: 0, coverage: 0, disabled: true });
  assert.deepEqual(matrixScore([0,1], [null,3]), { min: 3, max: 3, coverage: 1, disabled: false });
  assert.throws(() => matrixScore([1], [8]));
  assert.throws(() => matrixScore([1,1], [5]));
});

test('filtry łączą kryteria, tolerują polskie znaki; dopasowanie nie potwierdza przyjęcia', () => {
  const a = { id:'a', name:'Zarządzanie', universityId:'ue', language:'pl', fields:['ekonomia'], subjects:['matematyka'], subjectsVerified:true } as Programme;
  const b = { ...a, id:'b', language:'en', subjectsVerified:false } as Programme;
  assert.deepEqual(filterProgrammes([a,b], 'zarzadzanie', 'ue', 'pl').map(p => p.id), ['a']);
  assert.deepEqual(filterProgrammes([a,b], '', 'pwr', ''), []);
  const profile = emptyProfile();
  assert.match(matchSubjects(a, profile), /Wybierz/);
  profile.subjects.matematyka = 0;
  assert.match(matchSubjects(a, profile), /1 z 1/);
  assert.match(matchSubjects(b, profile), /Brak zweryfikowanej/);
});
