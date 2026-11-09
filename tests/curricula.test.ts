import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { curricula, validateCurricula } from '../src/curricula.ts';
import { presentCurriculum } from '../src/curriculumPresentation.ts';
const programmes = ['uwr', 'uew', 'pwr'].flatMap(id => JSON.parse(readFileSync(new URL(`../src/data/${id}.json`, import.meta.url), 'utf8')).programmes);

test('widok łączy grupy według semestrów i zachowuje przedmioty bez przypisanego semestru', () => {
  const group = (title: string, semester: string | null, subjects: string[]) => ({ title, semester, subjects, sourceUrl: 'https://example.com' });
  const groups = [group('strona 3', null, ['Łacina']), group('blok A', '2', ['Statystyka']), group('blok B', 'II', ['Język']), group('strona 4', '1 / 2. semestr', ['Projekt']), group('blok C', 'I', ['Matematyka'])];
  const result = presentCurriculum(groups);
  assert.deepEqual(result.sections.map(section => section.title), ['Semestr I', 'Semestry I / II', 'Semestr II']);
  assert.deepEqual(result.sections[2].subjects, ['Statystyka', 'Język']);
  assert.deepEqual(result.unknown, ['Łacina']);
  assert.deepEqual(presentCurriculum(groups, 'lacina').unknown, ['Łacina']);
  assert.equal(result.sections.reduce((sum, section) => sum + section.subjects.length, result.unknown.length), 5);
});

test('programy studiów: zakres ofert, pochodzenie list i brak mieszania stopni/trybów', () => {
  assert.deepEqual(validateCurricula(curricula, programmes), []);
  const economics = curricula.find(r => r.programmeId === 'uew-ekonomia')!;
  assert.equal(economics.referenceYear, '2026/2027');
  assert.equal(economics.completeness, 'full-plan');
  assert.ok(economics.groups.some(g => g.semester === 'V' && g.title.includes('Ekonomia menedżerska') && g.subjects.includes('Zarządzanie ryzykiem finansowym')));
  const business = curricula.find(r => r.programmeId === 'uew-international-business')!;
  assert.equal(business.specializations.length, 2);
  assert.ok(business.groups.some(g => g.subjects.includes('Financing the Global Space Economy')));
  assert.ok(curricula.filter(r => r.programmeId.startsWith('uew-')).every(r => r.groups.every(g => g.subjects.every(s => !/ - (?:N|PT)[12]\b/.test(s)))));
  const bad = structuredClone(curricula);
  bad[0].groups.push({ title: 'Bez podstawy', semester: null, subjects: ['Domyślny przedmiot'], sourceUrl: 'https://example.com' });
  assert.ok(validateCurricula(bad, programmes).length > 0);
});

test('plan informatyki stosowanej zachowuje cykl i semestry zajęć wielosemestralnych', () => {
  const plan = curricula.find(r => r.programmeId === 'uwr-informatyka-stosowana-i-systemy-pomiarowe')!;
  assert.equal(plan.completeness, 'full-plan');
  assert.ok(plan.referenceYear.includes('2025–2029'));
  assert.ok(plan.groups.some(group => group.semester === 'III, IV, V' && group.subjects.includes('Język obcy (poziom B2)')));
  assert.ok(plan.groups.some(group => group.semester === 'V, VI' && group.subjects.includes('Wychowanie fizyczne')));
  assert.ok(plan.groups.some(group => group.semester === 'I, II, III, IV' && group.subjects.some(subject => subject.includes('dla cudzoziemców'))));
});

test('odczyt PDF odrzuca efekty uczenia i akapity zamiast nazw zajęć', () => {
  const row = structuredClone(curricula.find(r => r.programmeId === 'uew-ekonomia')!);
  const scope = programmes.filter(p => p.id === row.programmeId);
  row.groups = [{ ...row.groups[0], subjects: [
    'zna zakres posiadanej przez siebie wiedzy i umiejętności z zakresu dziennikarstwa',
    'potrafi tworzyć teksty pisemne zróżnicowane gatunkowo',
    'Jest gotów do odpowiedzialnego pełnienia ról zawodowych',
    'Kurs to nie tylko podróż przez smaki i aromaty, ale eksploracja tożsamości',
    'Łącznie',
    'Łącznie:',
  ] }];
  assert.equal(validateCurricula([row], scope).length, 6);
  row.groups[0].subjects = ['Praktyczna nauka języka hiszpańskiego – egzamin [gramatyka praktyczna II + konwersacje i rozumienie ze słuchu II + język pisany II]', 'Total Quality Management'];
  assert.deepEqual(validateCurricula([row], scope), []);
});

test('instrukcja wyboru koszyka nie jest przedmiotem, zajęcia językowe pozostają dozwolone', () => {
  const row = structuredClone(curricula.find(r => r.programmeId === 'uew-ekonomia')!);
  const scope = programmes.filter(p => p.id === row.programmeId);
  row.groups[0].subjects = ['Student/ka wybiera jeden przedmiot z oferty Studium Języków Obcych'];
  assert.equal(validateCurricula([row], scope).length, 1);
  row.groups[0].subjects = ['Zajęcia uzupełniające - język angielski'];
  assert.deepEqual(validateCurricula([row], scope), []);
});

test('European Cultures ma wszystkie semestry, pule wyboru i warunkowy lektorat ze sprawdzonego planu', () => {
  const row = curricula.find(r => r.programmeId === 'uwr-european-cultures')!;
  assert.equal(row.completeness, 'full-plan');
  assert.ok(row.referenceYear.includes('2023/2024'));
  assert.equal(row.groups.reduce((sum, g) => sum + g.subjects.length, 0), 59);
  assert.equal(row.groups.filter(g => g.title.startsWith('Do wyboru')).length, 5);
  assert.ok(row.groups.some(g => g.semester === 'II, III, IV, V' && g.subjects.includes('Physical Education')));
  assert.ok(row.groups.some(g => g.title.includes('cudzoziemców') && g.subjects.includes('Polish Language Part I')));
  assert.ok(row.note.includes('co najmniej 5 ECTS'));
});

test('widok semestru zachowuje rozdział zajęć obowiązkowych, warunkowych i pul wyboru', () => {
  const row = curricula.find(r => r.programmeId === 'uwr-european-cultures')!;
  const result = presentCurriculum(row.groups);
  assert.deepEqual(result.sections[0].groups.map(g => g.title), ['Zajęcia obowiązkowe', 'Język polski dla cudzoziemców — część I', 'Do wyboru — jeden z dwóch przedmiotów']);
  assert.equal(result.sections[0].groups[2].subjects.length, 2);
  const filtered = presentCurriculum(row.groups, 'Warfare');
  assert.ok(filtered.sections.every(s => s.groups.every(g => g.title.startsWith('Do wyboru'))));
});
