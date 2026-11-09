import { test } from 'node:test';
import assert from 'node:assert/strict';
import { recommend } from '../src/recommendations.ts';
import { emptyProfile } from '../src/logic.ts';
import type { Programme } from '../src/types.ts';
import type { CurriculumRecord } from '../src/curriculumTypes.ts';

test('rekomendacje pokazują znane zgodności bez traktowania zaprzeczenia jako zainteresowania', () => {
  const programme: Programme = { id: 'p', universityId: 'u', name: 'Informatyka', language: 'pl', level: 'bachelor', city: 'Wrocław', duration: null, referenceYear: '2026', description: 'Badania danych', fields: [], subjects: ['matematyka'], subjectsVerified: true, admissionNote: '', sourceIds: [], thresholds: [], careers: [], careerNote: '' };
  const plan: CurriculumRecord = { programmeId: 'p', checkedAt: '2026-10-29', referenceYear: '2026', completeness: 'listed-subjects', groups: [{title: 'Plan', semester: null, subjects: ['Analiza danych'], sourceUrl: 'https://example.com'}], specializations: [], specializationStatus: 'not-found', note: '', sources: [] };
  const profile = { ...emptyProfile(), subjects: { matematyka: null }, interests: 'analiza danych', preferences: {tasks:['dane'], mobility:'any' as const, maxStudyYears:null, avoidShifts:false, strictMobility:false} };
  const result = recommend([programme], [plan], profile).results[0];
  assert.equal(result.evidence, 3);
  assert.deepEqual(result.subjectMatches, ['matematyka']);
  assert.ok(result.courseMatches.includes('analiza'));
  assert.ok(result.gaps.includes('Lista zajęć jest częściowa.'));
  const negative = recommend([programme], [plan], { ...profile, interests: 'nie lubię analizy danych' });
  assert.equal(negative.ambiguous, true);
  assert.equal(negative.results[0].evidence, 2);
  assert.deepEqual(recommend([programme], [plan], emptyProfile()).results, []);
});
