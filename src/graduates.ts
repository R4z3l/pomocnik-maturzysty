import data from './data/graduates.json' with { type: 'json' };
import type { GraduateData } from './graduateTypes.ts';
import type { Programme } from './types.ts';

export const graduateData = data as GraduateData;

export function outcomesFor(programmeId: string) {
  const match = graduateData.matches.find(item => item.programmeId === programmeId);
  const ids = new Set(match?.cohortIds);
  return { match, cohorts: graduateData.cohorts.filter(item => ids.has(item.id)) };
}

export function validateGraduateData(input: GraduateData, programmes: Programme[]): string[] {
  const errors: string[] = [];
  const cohortIds = new Set(input.cohorts.map(c => c.id));
  const matchedIds = new Set(input.matches.map(m => m.programmeId));
  if (cohortIds.size !== input.cohorts.length) errors.push('Duplikaty kohort ELA');
  if (matchedIds.size !== input.matches.length) errors.push('Duplikaty dopasowań ELA');
  if (input.graduationYear !== 2024) errors.push('Nowy rocznik ELA wymaga przeglądu importu i definicji');
  const used = new Set<string>();
  for (const match of input.matches) {
    const programme = programmes.find(p => p.id === match.programmeId);
    if (!programme || !match.cohortIds.length || !match.note) errors.push(`Nieprawidłowe dopasowanie: ${match.programmeId}`);
    for (const id of match.cohortIds) {
      const cohort = input.cohorts.find(c => c.id === id);
      if (!cohort || cohort.universityId !== programme?.universityId || cohort.level !== programme?.level) errors.push(`Nieprawidłowa kohorta: ${match.programmeId}/${id}`);
      if (used.has(id)) errors.push(`Kohorta przypisana wielokrotnie: ${id}`);
      used.add(id);
    }
  }
  for (const cohort of input.cohorts) {
    if (!used.has(cohort.id) || !cohort.reportName || !Number.isInteger(cohort.graduates) || cohort.graduates < 1) errors.push(`Tożsamość/liczebność kohorty: ${cohort.id}`);
    for (const key of ['inZus', 'medianSalary', 'meanSalary', 'relativeSalary', 'relativeUnemployment', 'unemploymentRisk', 'employmentPercent', 'furtherStudyPercent', 'jobSearchMonths', 'jobSearchNoExperienceMonths'] as const) {
      const value = cohort[key];
      if (value !== null && (!Number.isFinite(value) || value < 0)) errors.push(`Wartość ${cohort.id}/${key}`);
    }
    if (cohort.inZus !== null && (!Number.isInteger(cohort.inZus) || cohort.inZus > cohort.graduates)) errors.push(`Populacja ZUS: ${cohort.id}`);
    for (const key of ['unemploymentRisk', 'employmentPercent', 'furtherStudyPercent'] as const) {
      if (cohort[key] !== null && cohort[key]! > 100) errors.push(`Procent poza zakresem: ${cohort.id}/${key}`);
    }
  }
  return errors;
}
