import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { programmeDescriptions, validateProgrammeDescriptions } from '../src/descriptions.ts';
import type { Programme } from '../src/types.ts';

test('opisy wszystkich ofert mają właściwy język, poziom i zgodny dowód oficjalnego źródła', () => {
  const read = (path: string) => JSON.parse(readFileSync(new URL('../'+path, import.meta.url), 'utf8'));
  const programmes: Programme[] = ['uwr','uew','pwr','upwr','umw'].flatMap(uni => read('src/data/'+uni+'.json').programmes);
  assert.equal(programmeDescriptions.length, 215);
  assert.deepEqual(validateProgrammeDescriptions(programmeDescriptions, programmes), []);
  const audit = read('docs/research/descriptions/audit.json').records as {programmeId:string;language:string;level:string;url:string;file:string;sha256:string}[];
  assert.equal(audit.length,215);
  for (const row of programmeDescriptions) {
    const evidence = audit.find(a=>a.programmeId===row.programmeId)!;
    assert.ok(evidence,row.programmeId);
    assert.equal(evidence.url,row.sourceUrl);
    assert.equal(evidence.language,row.language);
    assert.equal(evidence.level,row.level);
    const bytes = readFileSync(new URL('../docs/research/descriptions/'+evidence.file,import.meta.url));
    assert.equal(createHash('sha256').update(bytes).digest('hex'),row.sourceHash,row.programmeId);
    assert.equal(evidence.sha256,row.sourceHash);
  }
  const health = programmeDescriptions.find(r=>r.programmeId==='umw-zdrowie-publiczne')!;
  assert.ok(health.careerRoles.includes('Analityk danych medycznych'));
  assert.ok(health.practice.some(text=>text.includes('NFZ')));
  assert.ok(health.notes.some(text=>text.includes('II stopnia')));
  assert.ok(!health.teachingForms.join(' ').includes('magisterskie'));
  assert.equal(programmeDescriptions.filter(r=>r.status==='limited-source').length,1);
  assert.equal(programmeDescriptions.find(r=>r.programmeId==='uwr-ochrona-srodowiska')!.sourceUrl,'https://msos.uwr.edu.pl/studia-pierwszego-stopnia/');
  assert.equal(programmeDescriptions.find(r=>r.programmeId==='upwr-weterynaria-w-jezyku-angielskim')!.topics.length,0);
  // Hospitality nie oznacza szpitala, technologist nie oznacza logistyka,
  // roboty budowlane nie oznaczają robotyki, a nazwa partnera nie jest zawodem.
  const careers = (id:string) => programmeDescriptions.find(r=>r.programmeId===id)!.careerAreas;
  assert.ok(!careers('uwr-european-cultures').includes('Placówki lecznicze'));
  assert.ok(!careers('uwr-biotechnology').includes('Logistyka i łańcuchy dostaw'));
  assert.ok(!careers('upwr-inzynieria-srodowiska').includes('Robotyka'));
  assert.ok(!careers('pwr-architektura').includes('Media i dziennikarstwo'));
  assert.ok(!careers('uew-informatyka-w-biznesie').includes('Ochrona i zarządzanie środowiskiem'));
  const invalid = structuredClone(programmeDescriptions);
  invalid[0].language = invalid[0].language==='pl'?'en':'pl';
  invalid[1].sourceUrl='https://example.com/';
  assert.ok(validateProgrammeDescriptions(invalid,programmes).some(error=>error.includes('język')));
  assert.ok(validateProgrammeDescriptions(invalid,programmes).some(error=>error.includes('spoza uczelni')));
});
