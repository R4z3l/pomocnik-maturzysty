import data from './data/programme-descriptions.json' with { type: 'json' };
import { sourceExclusion } from './sources.ts';
import type { Programme } from './types.ts';
import type { ProgrammeDescription } from './descriptionTypes.ts';

export const programmeDescriptions = data as ProgrammeDescription[];

export function validateProgrammeDescriptions(rows: ProgrammeDescription[], programmes: Programme[]): string[] {
  const errors: string[] = [];
  const seen = new Set<string>();
  const domains: Record<string, string> = {uwr:'uwr.edu.pl',uew:'uew.pl',pwr:'pwr.edu.pl',upwr:'upwr.edu.pl',umw:'umw.edu.pl'};
  for (const row of rows) {
    const fail = (message: string) => errors.push(`${row.programmeId}: ${message}`);
    const programme = programmes.find(p => p.id === row.programmeId);
    if (!programme) { fail('brak oferty'); continue; }
    if (seen.has(row.programmeId)) fail('powtórzony opis');
    seen.add(row.programmeId);
    if (row.language !== programme.language || row.level !== programme.level) fail('niezgodny język lub poziom');
    try {
      const url = new URL(row.sourceUrl);
      const domain = domains[programme.universityId];
      if (url.protocol !== 'https:' || !domain || !(url.hostname === domain || url.hostname.endsWith('.'+domain))) fail('źródło spoza uczelni');
      if (sourceExclusion(row.sourceUrl)) fail('źródło wykluczone');
    } catch { fail('błędny URL'); }
    if (!/^\d{4}-\d{2}-\d{2}$/.test(row.checkedAt) || !row.referenceYear || !row.sourceTitle || !/^[a-f0-9]{64}$/.test(row.sourceHash)) fail('niepełne pochodzenie danych');
    if (!['reviewed-source','limited-source'].includes(row.status)) fail('nieznany status');
    if (!row.overview.length || row.overview.some(p => !p.trim())) fail('brak streszczenia');
    for (const key of ['overview','topics','teachingForms','practice','careerAreas','careerRoles','specializations','sourceSections','notes'] as const) {
      if (!Array.isArray(row[key]) || row[key].some(value => typeof value !== 'string' || !value.trim())) fail('błędna lista '+key);
      else if (new Set(row[key]).size !== row[key].length) fail('powtórzone elementy '+key);
    }
  }
  for (const p of programmes) if (!seen.has(p.id)) errors.push(`${p.id}: brak opisu`);
  return errors;
}
