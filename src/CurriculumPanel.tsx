import { useState } from 'react';
import type { Programme } from './types';
import { curricula } from './curricula';
import { presentCurriculum } from './curriculumPresentation';
import './curriculum.css';

export default function CurriculumPanel({ programme }: { programme: Programme }) {
  const [query, setQuery] = useState('');
  const record = curricula.find(r => r.programmeId === programme.id);
  if (!record) return <p>Program studiów oczekuje na weryfikację źródłową.</p>;
  const { sections, unknown, unknownGroups } = presentCurriculum(record.groups, query);
  const matched = sections.reduce((sum, section) => sum + section.subjects.length, unknown.length);
  const count = record.groups.reduce((sum, group) => sum + group.subjects.length, 0);
  return <div className="curriculum-panel">
    <div className="curriculum-heading"><h3>Czego będziesz się uczyć?</h3><span className="tag">{record.completeness === 'full-plan' ? 'Spis z pełnego planu' : record.completeness === 'listed-subjects' ? 'Lista częściowa z uczelni' : 'Spis jeszcze niepotwierdzony'}</span></div>
    <p className="curriculum-year">Rok programu: <strong>{record.referenceYear}</strong> · sprawdzono {record.checkedAt}</p>
    {record.completeness === 'unavailable' && <p>Nie potwierdzono aktualnego spisu przedmiotów dla tej oferty. Szczegóły sprawdzenia znajdziesz poniżej w źródłach.</p>}
    {record.completeness !== 'unavailable' && <p className="curriculum-context">Plan dotyczy wskazanego cyklu kształcenia. Przedmioty i dostępność specjalności dla osób rozpoczynających studia w 2027 roku mogą się zmienić. Zajęcia do wyboru i alternatywne ścieżki nie są obowiązkowe dla każdego studenta.</p>}
    {count > 0 && <><label className="curriculum-search">Znajdź przedmiot w tym programie<input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder="np. statystyka, programowanie, język…"/></label><p className="muted">Pozycje w spisie: {count}{query ? ` · pasuje ${matched}` : ''}. Ten sam przedmiot może występować w kilku semestrach.</p><div className="curriculum-groups">{sections.map((section, index) => <details key={section.title} open={query ? true : index === 0}><summary>{section.title}<small>Pozycje: {section.subjects.length}</small></summary><div>{section.groups.map((group, groupIndex) => <div className="curriculum-subgroup" key={groupIndex}><h4>{group.title}</h4><ul>{group.subjects.map((subject, i) => <li key={`${subject}-${i}`}>{subject}</li>)}</ul></div>)}</div></details>)}{unknown.length > 0 && <><p className="muted">{sections.length ? 'Dla poniższych przedmiotów nie potwierdzono semestru.' : 'Nie potwierdzono przypisania przedmiotów do semestrów.'}</p>{unknownGroups.map((group, groupIndex) => <div className="curriculum-subgroup" key={groupIndex}><h4>{group.title}</h4><ul>{group.subjects.map((subject, i) => <li key={`${subject}-${i}`}>{subject}</li>)}</ul></div>)}</>}</div>{matched === 0 && <p role="status">Brak przedmiotów pasujących do wyszukiwania.</p>}</>}
    <section className="curriculum-specializations"><h3>Specjalności, specjalizacje i ścieżki</h3>{record.specializations.length ? <><p className="muted">Nazewnictwo zachowuje rozróżnienia stosowane przez uczelnię. Uruchomienie wariantu może zależeć od liczby chętnych.</p><ul>{record.specializations.map(s => <li key={`${s.kind}-${s.name}`}><span className="curriculum-kind">{s.kind}</span><strong>{s.name}</strong>{s.note && <p>{s.note}</p>}<a href={s.sourceUrl} target="_blank" rel="noreferrer">Potwierdzenie na stronie uczelni ↗</a></li>)}</ul></> : <p>{record.specializationStatus === 'none-confirmed' ? 'Uczelnia potwierdza brak odrębnych specjalności w tym programie.' : 'Nie potwierdzono listy specjalności w zebranych materiałach. To nie oznacza, że kierunek ich nie oferuje.'}</p>}</section>
    <details className="curriculum-sources"><summary>Zakres, programy i źródła uczelni</summary><p>{record.note}</p><ul>{record.sources.map(s => <li key={s.url}><a href={s.url} target="_blank" rel="noreferrer">{s.title} ↗</a><small>{s.year}</small><p>{s.note}</p></li>)}</ul></details>
  </div>;
}

export function CurriculumCoverage() {
  const withSubjects = curricula.filter(r => r.groups.some(g => g.subjects.length));
  return <section className="panel"><h2>Przedmioty i specjalności — pokrycie</h2><p>{withSubjects.length} ze {curricula.length} ofert ma zapisany spis przedmiotów, w tym {curricula.filter(r => r.completeness === 'full-plan').length} z pełnego planu. Pozostałe spisy są częściowe albo oznaczone jako brak potwierdzenia. {curricula.filter(r => r.specializations.length).length} ofert ma potwierdzone specjalności, ścieżki lub moduły.</p><p className="muted">Dane pochodzą ze stron i dokumentów uczelni w katalogu; rocznik oraz link do planu są na zakładce „Program i specjalności” każdego kierunku.</p></section>;
}
