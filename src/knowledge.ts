import type { Catalogue } from './types.ts';
import type { CurriculumRecord } from './curriculumTypes.ts';

export function knowledgeCoverage(catalogue: Catalogue, curricula: CurriculumRecord[], graduateIds: string[]) {
  const graduates = new Set(graduateIds);
  const plans = new Map(curricula.map(row => [row.programmeId, row]));
  return catalogue.universities.map(university => {
    const programmes = catalogue.programmes.filter(p => p.universityId === university.id);
    return {
      id: university.id, name: university.name, total: programmes.length,
      calculators: programmes.filter(p => p.admissionRuleId).length,
      withDuration: programmes.filter(p => p.duration !== null).length,
      withThresholds: programmes.filter(p => p.thresholds.length > 0).length,
      fullPlans: programmes.filter(p => plans.get(p.id)?.completeness === 'full-plan').length,
      partialPlans: programmes.filter(p => plans.get(p.id)?.completeness === 'listed-subjects').length,
      missingPlans: programmes.filter(p => !plans.has(p.id) || plans.get(p.id)?.completeness === 'unavailable').length,
      withGraduates: programmes.filter(p => graduates.has(p.id)).length,
    };
  });
}
