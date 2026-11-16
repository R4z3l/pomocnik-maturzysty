import a from './data/curricula-uwr-a.json' with { type: 'json' };
import b from './data/curricula-uwr-b.json' with { type: 'json' };
import uew from './data/curricula-uew.json' with { type: 'json' };
import pwr from './data/curricula-pwr.json' with { type: 'json' };
import upwr from './data/curricula-upwr.json' with { type: 'json' };
import umw from './data/curricula-umw.json' with { type: 'json' };
import type { CurriculumRecord } from './curriculumTypes.ts';
import type { Programme } from './types.ts';
import { sourceExclusion } from './sources.ts';

export const curricula = [...a, ...b, ...uew, ...pwr, ...upwr, ...umw] as CurriculumRecord[];

export function validateCurricula(records: CurriculumRecord[], programmes: Programme[]) {
  const errors: string[] = [];
  const ids = new Set(records.map(r => r.programmeId));
  if (ids.size !== records.length) errors.push('Powtórzone programy studiów');
  for (const p of programmes) if (!ids.has(p.id)) errors.push(`Brak kontroli programu: ${p.id}`);
  for (const row of records) {
    if (!programmes.some(p => p.id === row.programmeId)) errors.push(`Nieznana oferta: ${row.programmeId}`);
    const urls = new Set(row.sources.map(s => s.url));
    if (urls.size !== row.sources.length) errors.push(`Powtórzone źródło programu: ${row.programmeId}`);
    if (!row.sources.length || !row.referenceYear || !row.note || !/^\d{4}-\d{2}-\d{2}$/.test(row.checkedAt)) errors.push(`Metadane programu: ${row.programmeId}`);
    if (!['full-plan','listed-subjects','unavailable'].includes(row.completeness)) errors.push(`Status programu: ${row.programmeId}`);
    if (row.completeness !== 'unavailable' && !row.groups.some(g => g.subjects.length)) errors.push(`Pusty spis: ${row.programmeId}`);
    if (row.completeness === 'unavailable' && row.groups.some(g => g.subjects.length)) errors.push(`Spis oznaczony jako brak danych: ${row.programmeId}`);
    if (!['listed','none-confirmed','not-found'].includes(row.specializationStatus)) errors.push(`Nieznany status specjalności: ${row.programmeId}`);
    if ((row.specializationStatus === 'listed') !== (row.specializations.length > 0)) errors.push(`Status specjalności: ${row.programmeId}`);
    for (const source of row.sources) {
      const host = new URL(source.url).hostname;
      if (!['uwr.edu.pl','uni.wroc.pl','uew.pl','ue.wroc.pl','ue.e-sylabus.pl','pwr.edu.pl','upwr.edu.pl','umw.edu.pl'].some(domain => host === domain || host.endsWith('.'+domain))) errors.push(`Nieoficjalne źródło programu: ${source.url}`);
      if (sourceExclusion(source.url) || !source.title || !source.year || !source.note) errors.push(`Źródło programu: ${row.programmeId}/${source.url}`);
    }
    for (const group of row.groups) if (!urls.has(group.sourceUrl) || !group.title || group.subjects.some(s => !s.trim())) errors.push(`Przedmioty bez źródła: ${row.programmeId}`);
    for (const group of row.groups) for (const subject of group.subjects) {
      if (/^Student(?:\/ka|ka)? wybiera\b/i.test(subject)) errors.push(`Instrukcja wyboru zamiast przedmiotu: ${row.programmeId}/${subject}`);
      if (/^(?:(?:Łącznie|Razem|Suma|Total):?|ECTS|dyscyplina\/punkty ECTS|Przedmiot:\s*obowiązkowy.*|Cele kształcenia, wskazanie związku.*)$/i.test(subject)) errors.push(`Nagłówek zamiast przedmiotu: ${row.programmeId}/${subject}`);
      if (/^(?:zna zakres posiadanej|potrafi |jest gotów do |kurs to nie tylko podróż|opcyjne obejmują:)/i.test(subject) || subject.length > 400 && subject.includes('. ')) errors.push(`Opis lub efekt uczenia zamiast przedmiotu: ${row.programmeId}/${subject}`);
    }
    for (const special of row.specializations) if (!urls.has(special.sourceUrl) || !special.name || !['specjalność','specjalizacja','ścieżka','moduł'].includes(special.kind)) errors.push(`Specjalność bez źródła: ${row.programmeId}`);
  }
  return errors;
}
