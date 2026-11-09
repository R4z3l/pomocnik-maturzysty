import type { CurriculumRecord } from './curriculumTypes.ts';
import type { Programme, Profile } from './types.ts';
import { suggestedFamilies } from './careers.ts';

const normalize = (s: string) => s.toLocaleLowerCase('pl').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ł/g, 'l');
const words = (s: string) => normalize(s).match(/[a-z0-9]+/g) ?? [];
const ignored = new Set(['oraz', 'jest', 'lubię', 'lubie', 'interesuje', 'interesuja', 'moje', 'chce', 'studiow', 'studia', 'praca', 'pracy', 'kierunek', 'jestem', 'bardzo', 'ktore', 'ktorych']);

export function recommend(programmes: Programme[], curricula: CurriculumRecord[], profile: Profile) {
  // Nie próbujemy interpretować zaprzeczeń i długich zdań jak deklaracji zainteresowań.
  const interestWords = words(profile.interests);
  const ambiguous = interestWords.some(word => ['nie', 'bez', 'unikam', 'nienawidze'].includes(word));
  const interests = ambiguous ? [] : [...new Set(interestWords.filter(w => w.length >= 4 && !ignored.has(w)))].slice(0, 15);
  const selected = Object.keys(profile.subjects);
  const tasks = profile.preferences?.tasks ?? [];
  return {
    ambiguous,
    results: programmes.map(programme => {
      const curriculum = curricula.find(record => record.programmeId === programme.id);
      const descriptions = new Set(words([programme.name, programme.description, ...programme.fields].join(' ')));
      const courseNames = curriculum?.groups.flatMap(group => group.subjects) ?? [];
      const courseWords = new Set(words(courseNames.join(' ')));
      const subjectMatches = programme.subjectsVerified ? programme.subjects.filter(subject => selected.includes(subject)) : [];
      const interestMatches = interests.filter(word => descriptions.has(word));
      const courseMatches = interests.filter(word => courseWords.has(word));
      const careerFamilies = suggestedFamilies(programme);
      const taskMatches = [...new Set(careerFamilies.flatMap(family => family.tasks.filter(task => tasks.includes(task))))];
      const evidence = Number(subjectMatches.length > 0) + Number(interestMatches.length > 0 || courseMatches.length > 0) + Number(taskMatches.length > 0);
      const gaps: string[] = [];
      if (!selected.length) gaps.push('Nie wybrano rozszerzeń w profilu.');
      else if (Object.values(profile.subjects).some(value => value === null)) gaps.push('Nie podano wszystkich wyników wybranych rozszerzeń.');
      if (!programme.subjectsVerified) gaps.push('Brak zweryfikowanej listy punktowanych przedmiotów.');
      if (!programme.admissionRuleId) gaps.push('Brak automatycznej reguły rekrutacji dla tej oferty.');
      if (!profile.interests.trim()) gaps.push('Nie wpisano zainteresowań.');
      if (ambiguous) gaps.push('Zainteresowania zawierają zaprzeczenie; porównanie słów pominięto.');
      if (!ambiguous && profile.interests.trim() && !interests.length) gaps.push('Brak rozpoznanych konkretnych słów zainteresowań.');
      if (!courseNames.length) gaps.push('Brak potwierdzonej listy zajęć.');
      else if (curriculum?.completeness !== 'full-plan') gaps.push('Lista zajęć jest częściowa.');
      if (!tasks.length) gaps.push('Nie wybrano rodzaju preferowanych zadań.');
      if (tasks.length && !careerFamilies.length) gaps.push('Brak automatycznie sugerowanej rodziny zawodów.');
      return { programme, subjectMatches, interestMatches, courseMatches, taskMatches, familyNames: careerFamilies.filter(family => family.tasks.some(task => tasks.includes(task))).map(family => family.name), evidence, gaps };
    }).filter(result => result.evidence > 0).sort((a, b) => b.evidence - a.evidence || a.programme.name.localeCompare(b.programme.name, 'pl') || a.programme.universityId.localeCompare(b.programme.universityId)),
  };
}

