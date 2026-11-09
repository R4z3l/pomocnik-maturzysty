import { useState } from 'react';
import type { Programme } from './types';
import { graduateData, outcomesFor } from './graduates';
import './graduates.css';

const number = new Intl.NumberFormat('pl-PL', { maximumFractionDigits: 2 });
function value(amount: number | null, unit = '') {
  return amount === null ? 'Brak opublikowanej wartości' : `${number.format(amount)}${unit ? ` ${unit}` : ''}`;
}

function GraduateSources() {
  return <details className="graduate-sources">
    <summary>Źródło i definicje wskaźników</summary>
    <p>Edycja: {graduateData.edition} · sprawdzono {graduateData.checkedAt}.</p>
    <nav aria-label="Źródła danych ELA">
      <a href={graduateData.sourceUrl} target="_blank" rel="noreferrer">Oficjalne dane ELA ↗</a>
      <a href={graduateData.dictionaryUrl} target="_blank" rel="noreferrer">Słownik zmiennych ↗</a>
      <a href={graduateData.methodologyUrl} target="_blank" rel="noreferrer">Opis metody — edycja 10 (2025) ↗</a>
      <a href={graduateData.citationUrl} target="_blank" rel="noreferrer">Informacja o cytowaniu ↗</a>
    </nav>
    <p>Strona ELA edycji 11 nadal odsyła do opisu metody z edycji 10. Zakres wskaźników P1 potwierdza bieżący słownik; starszy PDF objaśnia sposób pomiaru. Puste pole CSV nie wyjaśnia przyczyny braku — nie odtwarzamy utajnionych wyników.</p><p className="graduate-citation">{graduateData.citation}</p>
  </details>;
}

export default function GraduateOutcomesPanel({ programme }: { programme: Programme }) {
  const { match, cohorts } = outcomesFor(programme.id);
  const [selectedId, setSelectedId] = useState(cohorts[0]?.id ?? '');
  const cohort = cohorts.find(row => row.id === selectedId) ?? cohorts[0];
  return <section className="graduate-panel" aria-label="Losy absolwentów ELA">
    <div className="graduate-heading"><span className="graduate-eyebrow">Ogólnopolski system monitorowania Ekonomicznych Losów Absolwentów</span>
      <h3>Losy absolwentów — ELA</h3>
      <p>Rocznik ukończenia studiów: <strong>{graduateData.graduationYear}</strong>. Okres obserwacji: {graduateData.observation}.</p>
    </div>
    {!match || !cohort ? <div className="graduate-gap"><strong>Brak dopasowanych danych dla tego kierunku</strong><p>W lokalnym zestawieniu nie ma potwierdzonej grupy absolwentów odpowiadającej tej ofercie. To luka danych, a nie zerowe wynagrodzenie, brak pracy ani ocena kierunku.</p></div> : <>
      {match.note && <p className="graduate-match-note">{match.note}</p>}
      {cohorts.length > 1 && <div className="graduate-picker"><label htmlFor={`graduate-cohort-${programme.id}`}>Wariant programu w ELA</label>
        <select id={`graduate-cohort-${programme.id}`} value={cohort.id} onChange={event => setSelectedId(event.target.value)}>{cohorts.map(row => <option key={row.id} value={row.id}>{[row.reportName, row.unit, row.specialty, `ID: ${row.id}`].filter(Boolean).join(' · ')}</option>)}</select>
        <p>Każda grupa jest prezentowana osobno. Nie sumujemy grup ani nie uśredniamy ich median.</p>
      </div>}
      <div className="graduate-cohort"><strong>{cohort.reportName}</strong>{cohort.unit && <span>{cohort.unit}</span>}{cohort.specialty && <span>Specjalność: {cohort.specialty}</span>}<span>{cohort.level === 'long-cycle' ? 'Jednolite studia magisterskie' : 'Studia pierwszego stopnia'} · ID ELA: {cohort.id}</span></div>
      <div className="graduate-population"><span>Absolwenci w grupie <strong>{value(cohort.graduates)}</strong></span><span>Osoby widoczne w rejestrach ZUS <strong>{value(cohort.inZus)}</strong></span></div>
      <p className="graduate-note">Liczba absolwentów i liczba osób w ZUS opisują różne populacje. Wskaźnik wynagrodzenia nie opisuje zarobków całej grupy absolwentów.</p>
      <div className="graduate-metrics">
        <article><h4>Mediana średnich miesięcznych wynagrodzeń brutto</h4><strong>{value(cohort.medianSalary, 'zł')}</strong><p>Pierwszy rok po dyplomie; wszystkie źródła wynagrodzenia rejestrowane przez ZUS. Każdej osobie uwzględnia się miesiące zatrudnienia. Osoby bez pracy nie wchodzą do mediany; dochodów z samozatrudnienia ELA nie zna.</p></article>
        <article><h4>Średni czas do pierwszej pracy</h4><strong>{value(cohort.jobSearchMonths, 'mies.')}</strong><p>Wśród osób, które podjęły pracę po dyplomie; cały okres badania kohorty, nie tylko P1. Nie jest to czas szukania pracy zgodnej z dyplomem.</p></article>
        <article><h4>Ryzyko bezrobocia</h4><strong>{value(cohort.unemploymentRisk, '%')}</strong><p>Średni odsetek miesięcy z rejestracją jako bezrobotny w pierwszym roku po dyplomie. To nie odsetek osób bez pracy.</p></article>
      </div>
      <details className="graduate-more"><summary>Pozostałe opublikowane wskaźniki</summary><dl>
        <div><dt>Względny wskaźnik zarobków (WWZ)</dt><dd>{value(cohort.relativeSalary)}</dd></div>
        <div><dt>Względny wskaźnik bezrobocia (WWB)</dt><dd>{value(cohort.relativeUnemployment)}</dd></div>
        <div><dt>Średnie miesięczne wynagrodzenie brutto</dt><dd>{value(cohort.meanSalary, 'zł')}</dd></div>
        <div><dt>Pracowali choć raz w pierwszym roku po dyplomie</dt><dd>{value(cohort.employmentPercent, '%')}</dd></div>
        <div><dt>Podjęli studia II stopnia w pierwszym roku po dyplomie</dt><dd>{value(cohort.furtherStudyPercent, '%')}</dd></div>
        <div><dt>Czas do pierwszej pracy bez wcześniejszego doświadczenia</dt><dd>{value(cohort.jobSearchNoExperienceMonths, 'mies.')}</dd></div>
      </dl><p className="graduate-note">WWZ i WWB dotyczą pierwszego roku po dyplomie. Wartość 1 oznacza lokalny punkt odniesienia w powiecie zamieszkania: WWZ powyżej 1 to wyższe zarobki, WWB poniżej 1 to niższe ryzyko rejestrowanego bezrobocia. Są to średnie indywidualnych ilorazów, a nie procenty. Dalsze studia po licencjacie wpływają na aktywność zawodową — niskie zarobki nie muszą oznaczać słabych perspektyw.</p></details>
    </>}
    <p className="graduate-caution">To historyczne losy konkretnego rocznika, a nie prognoza przyszłego wynagrodzenia. Dane nie potwierdzają, że absolwenci pracują w zawodzie zgodnym z dyplomem. Brak opublikowanej wartości nie oznacza zera.</p>
    <GraduateSources />
  </section>;
}

export function GraduateCoverage() {
  return <section className="graduate-coverage"><h3>Pokrycie danych ELA</h3><p>Dopasowane oferty: {number.format(graduateData.matches.length)} ze 109. Osobne grupy absolwentów: {number.format(graduateData.cohorts.length)}. Rocznik: {graduateData.graduationYear}; okres obserwacji: {graduateData.observation}.</p><p>Brak dopasowania może wynikać z różnic w nazwie, poziomie, jednostce lub specjalności albo z braku odpowiedniej grupy w publikacji (np. nowy kierunek lub mała grupa). Przyczyna konkretnego braku nie zawsze jest ustalona. Nie zastępujemy tych luk danymi podobnego kierunku.</p><GraduateSources /></section>;
}
