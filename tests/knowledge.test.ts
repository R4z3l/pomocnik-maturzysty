import { test } from 'node:test';
import assert from 'node:assert/strict';
import { knowledgeCoverage } from '../src/knowledge.ts';
import type { Catalogue, Programme } from '../src/types.ts';

test('raport pokrycia rozróżnia brak, częściowy plan i pełny plan oraz ignoruje stare dopasowania ELA', () => {
  const programmes = [{ id: 'a', universityId: 'u', duration: null, thresholds: [], admissionRuleId: 'rule' }, { id: 'b', universityId: 'u', duration: '6 semestrów', thresholds: [{ value: 0 }] }, { id: 'c', universityId: 'u', duration: '6 semestrów', thresholds: [] }] as Programme[];
  const data = { universities: [{ id: 'u', name: 'Uczelnia' }], programmes } as Catalogue;
  const plans = [{ programmeId: 'a', completeness: 'full-plan' }, { programmeId: 'b', completeness: 'listed-subjects' }] as Parameters<typeof knowledgeCoverage>[1];
  const [row] = knowledgeCoverage(data, plans, ['a', 'old']);
  assert.deepEqual({ ...row, name: undefined }, { id: 'u', name: undefined, total: 3, calculators: 1, withDuration: 2, withThresholds: 1, fullPlans: 1, partialPlans: 1, missingPlans: 1, withGraduates: 1 });
});
