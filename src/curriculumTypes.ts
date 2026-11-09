export interface CurriculumSource {
  title: string;
  url: string;
  year: string;
  note: string;
}
export interface CurriculumRecord {
  programmeId: string;
  checkedAt: string;
  referenceYear: string;
  completeness: 'full-plan' | 'listed-subjects' | 'unavailable';
  groups: { title: string; semester: string | null; subjects: string[]; sourceUrl: string }[];
  specializations: { name: string; kind: 'specjalność' | 'specjalizacja' | 'ścieżka' | 'moduł'; note: string; sourceUrl: string }[];
  specializationStatus: 'listed' | 'none-confirmed' | 'not-found';
  note: string;
  sources: CurriculumSource[];
}
