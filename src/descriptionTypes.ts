export interface ProgrammeDescription {
  programmeId: string;
  language: 'pl' | 'en';
  level: 'bachelor' | 'long-cycle';
  checkedAt: string;
  referenceYear: string;
  overview: string[];
  topics: string[];
  teachingForms: string[];
  practice: string[];
  careerAreas: string[];
  careerRoles: string[];
  specializations: string[];
  sourceSections: string[];
  sourceUrl: string;
  sourceTitle: string;
  sourceHash: string;
  status: 'reviewed-source' | 'limited-source';
  notes: string[];
}
