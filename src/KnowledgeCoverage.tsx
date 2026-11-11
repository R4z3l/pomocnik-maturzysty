import { catalogue } from './catalogue';
import { curricula } from './curricula';
import { graduateData } from './graduates';
import { knowledgeCoverage } from './knowledge';

export default function KnowledgeCoverage() {
  const rows = knowledgeCoverage(catalogue, curricula, graduateData.matches.map(row => row.programmeId));
  return <section className="panel" aria-label="Stan bazy wiedzy"><h2>Stan bazy wiedzy</h2>
    <p>Każda liczba dotyczy ofert w aktualnym katalogu. Spis częściowy, brak danych i pełny plan mają osobne oznaczenia. Brak progu albo danych absolwentów nie jest oceną kierunku.</p>
    {rows.map(row => <details key={row.id}><summary>{row.name} — {row.total} ofert</summary><dl className="facts">
      <div><dt>Kalkulator punktów</dt><dd>{row.calculators} / {row.total}</dd></div>
      <div><dt>Potwierdzony czas studiów</dt><dd>{row.withDuration} / {row.total}</dd></div>
      <div><dt>Co najmniej jeden próg z naborów 2024–2026</dt><dd>{row.withThresholds} / {row.total}</dd></div>
      <div><dt>Pełny plan zajęć wskazanego cyklu</dt><dd>{row.fullPlans}</dd></div>
      <div><dt>Częściowy spis zajęć</dt><dd>{row.partialPlans}</dd></div>
      <div><dt>Bez potwierdzonego spisu zajęć</dt><dd>{row.missingPlans}</dd></div>
      <div><dt>Dopasowane dane absolwentów</dt><dd>{row.withGraduates} / {row.total}</dd></div>
    </dl></details>)}
    <p>Roczniki oferty, programu, zasad i progów sprawdzaj osobno na karcie. Pełny plan starszego cyklu nie potwierdza programu naboru 2027/28.</p>
    <p>Aktualizację z internetu bez AI można uruchomić na komputerze z projektem. Sposób pobierania, raport zmian oraz zakres automatyzacji opisano w „Instrukcjach” → „Aktualizacja bazy bez AI”. Strona nie pobiera danych w tle.</p>
  </section>;
}
