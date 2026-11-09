import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseThresholds } from '../src/thresholds.ts';
test('pełne tabele PWr: rowspan, tury, filie, przypisy, zero i nieuruchomione', () => {
  const raw = JSON.parse(readFileSync(new URL('../src/data/pwr-thresholds-raw.json', import.meta.url), 'utf8'));
  const rows = parseThresholds(raw.tables);
  assert.equal(rows.length, (66+67+65+65+64)*3);
  assert.equal(rows.filter(r => r.programme === 'Informatyka techniczna' && r.inScope && r.year === '2026/2027' && r.round === 'I tura')[0].value, 279.6);
  assert.equal(rows.filter(r => r.programme === 'Budownictwo' && r.inScope && r.year === '2026/2027' && r.round === 'I tura')[0].value, 193);
  assert.ok(rows.some(r => r.value === 0));
  assert.ok(rows.some(r => r.status === 'not-opened' && r.value === null));
  assert.ok(rows.some(r => r.faculty.includes('Wałbrzychu') && !r.inScope));
  assert.ok(rows.every(r => r.faculty.length && r.programme.length));
  assert.ok(rows.filter(r => !r.raw).every(r => r.status === 'missing' && r.value === null));
  const broken = structuredClone(raw.tables);
  broken[0].rows[1][2].text = 'nieznany format';
  assert.throws(() => parseThresholds(broken));
});
