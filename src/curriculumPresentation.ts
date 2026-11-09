import type { CurriculumRecord } from './curriculumTypes';

const roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'];
const normalize = (value: string) => value.toLocaleLowerCase('pl').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ł/g, 'l');

function semesterNumbers(value: string | null): number[] | null {
  if (!value) return null;
  const parts = value.toUpperCase().replace(/\.\s*SEMESTR\b/g, '').trim().split(/\s*[,/]\s*/);
  const numbers = parts.map(part => /^\d+$/.test(part) ? Number(part) : roman.indexOf(part) + 1);
  if (!numbers.length || numbers.some(number => number < 1 || number > roman.length)) return null;
  return [...new Set(numbers)].sort((a, b) => a - b);
}

export function presentCurriculum(groups: CurriculumRecord['groups'], query = '') {
  type SubjectGroup = { title: string; subjects: string[] };
  const sections = new Map<string, { title: string; semesters: number[]; subjects: string[]; groups: SubjectGroup[] }>();
  const unknown: string[] = [];
  const unknownGroups: SubjectGroup[] = [];
  const search = normalize(query);
  for (const group of groups) {
    const subjects = group.subjects.filter(subject => normalize(subject).includes(search));
    const semesters = semesterNumbers(group.semester);
    if (!semesters) { unknown.push(...subjects); if (subjects.length) unknownGroups.push({ title: group.title, subjects }); continue; }
    if (!subjects.length) continue;
    const key = semesters.join(',');
    const section = sections.get(key) ?? { title: `${semesters.length === 1 ? 'Semestr' : 'Semestry'} ${semesters.map(number => roman[number - 1]).join(' / ')}`, semesters, subjects: [], groups: [] };
    section.subjects.push(...subjects);
    section.groups.push({ title: group.title, subjects });
    sections.set(key, section);
  }
  return { sections: [...sections.values()].sort((a, b) => a.semesters[0] - b.semesters[0] || a.semesters.length - b.semesters.length || a.title.localeCompare(b.title)), unknown, unknownGroups };
}
