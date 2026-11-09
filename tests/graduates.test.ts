import { test } from 'node:test';
import assert from 'node:assert/strict';
import { graduateData, outcomesFor, validateGraduateData } from '../src/graduates.ts';
import { readFileSync } from 'node:fs';
const programmes = ['uwr', 'uew'].flatMap(id => JSON.parse(readFileSync(new URL(`../src/data/${id}.json`, import.meta.url), 'utf8')).programmes);

test('ELA: prawdziwe kohorty, osobne warianty i brak danych bez imputacji', () => {
  assert.deepEqual(validateGraduateData(graduateData, programmes), []);
  const admin = outcomesFor('uwr-administracja').cohorts;
  assert.equal(admin.length, 1);
  assert.equal(admin[0].medianSalary, 3093.93);
  assert.equal(admin[0].graduates, 83);
  assert.equal(outcomesFor('uwr-historia-sztuki').cohorts[0].medianSalary, null);
  const it = outcomesFor('uwr-informatyka').cohorts;
  assert.equal(it.length, 2);
  assert.notEqual(it[0].reportName, it[1].reportName);
  assert.equal(it.find(c => c.id === '29081')?.relativeUnemployment, 0);
  assert.equal(outcomesFor('uwr-chemistry').cohorts.length, 0);
  assert.equal(outcomesFor('nieistniejacy').match, undefined);
  const bad = structuredClone(graduateData);
  bad.cohorts[0].medianSalary = -1;
  bad.matches[0].cohortIds.push('nieistniejaca');
  assert.ok(validateGraduateData(bad, programmes).length >= 2);
});
