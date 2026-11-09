import { test } from 'node:test';
import assert from 'node:assert/strict';
import { families } from '../src/careers.ts';
import { jobSearchLinks } from '../src/jobSearch.ts';
import { displayJobStatus } from '../src/jobStatus.ts';

test('każda rodzina ma osobne wyszukiwania staży i pierwszej pracy we Wrocławiu', () => {
  for (const family of families) {
    const searches = jobSearchLinks(family.id);
    assert.deepEqual(searches.map(search => search.label), ['Praktyki i staże', 'Pierwsza praca']);
    assert.ok(searches.every(search => search.portals.length === 2 && search.portals.every(portal => new URL(portal.url).protocol === 'https:')));
    assert.ok(searches.every(search => search.portals.every(portal => decodeURIComponent(portal.url).toLowerCase().includes('wroc'))));
  }
  assert.deepEqual(jobSearchLinks('nieznany'), []);
});

test('oferta po ostatnim dniu ważności trafia do archiwum, bez zmiany zapisanych danych', () => {
  const job = { active: 'confirmed', expiresAt: '2026-11-25' };
  assert.equal(displayJobStatus(job, '2026-11-25'), 'confirmed');
  assert.equal(displayJobStatus(job, '2026-11-26'), 'expired');
  assert.equal(job.active, 'confirmed');
  assert.equal(displayJobStatus({ active: 'unconfirmed', expiresAt: null }, '2026-11-26'), 'unconfirmed');
});
