export interface GraduateCohort {
  id: string;
  universityId: string;
  name: string;
  reportName: string;
  unit: string;
  specialty: string;
  level: 'bachelor' | 'long-cycle';
  graduates: number;
  inZus: number | null;
  medianSalary: number | null;
  meanSalary: number | null;
  relativeSalary: number | null;
  relativeUnemployment: number | null;
  unemploymentRisk: number | null;
  employmentPercent: number | null;
  furtherStudyPercent: number | null;
  jobSearchMonths: number | null;
  jobSearchNoExperienceMonths: number | null;
}

export interface GraduateMatch {
  programmeId: string;
  cohortIds: string[];
  note: string;
}

export interface GraduateData {
  checkedAt: string;
  graduationYear: number;
  edition: string;
  observation: string;
  sourceUrl: string;
  dictionaryUrl: string;
  methodologyUrl: string;
  citationUrl: string;
  citation: string;
  cohorts: GraduateCohort[];
  matches: GraduateMatch[];
}
