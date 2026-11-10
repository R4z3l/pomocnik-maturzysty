import { useMemo, useState } from 'react';
import { admissionRules, catalogue } from './catalogue';
import { filterProgrammes } from './logic';
import { MATCHING_HISTORY_YEAR, matchMatura } from './maturaMatching';
import { sourceExclusion } from './sources';
import type { Profile } from './types';
import './matura-matching.css';

const number = (value: number) => value.toLocaleString('pl', { maximumFractionDigits: 2 });

export default function MaturaMatchingPanel({ profile, editProfile, open }: {
  profile: Profile; editProfile: () => void; open: (id: string, button: HTMLButtonElement) => void;
}) {
  const [query, setQuery] = useState('');
  const [university, setUniversity] = useState('');
  const [language, setLanguage] = useState('');
  const [reachedOnly, setReachedOnly] = useState(false);
  const [matchedOnly, setMatchedOnly] = useState(false);
  const [all, setAll] = useState(false);
  const results = useMemo(() => matchMatura(catalogue.programmes, admissionRules, profile), [profile]);
  const ids = new Set(filterProgrammes(catalogue.programmes, query, university, language).map(p => p.id));
  const filtered = results.filter(r => ids.has(r.programme.id) && (!reachedOnly || r.reachesThreshold) && (!matchedOnly || (r.fit?.ratio ?? 0) > 0));
  const selected = Object.keys(profile.subjects);
  const known = Object.values(profile.subjects).filter(v => v !== null).length;
  const visible = all ? filtered : filtered.slice(0, 20);
  return <section className="matura-matching" aria-label="Dopasowanie matury">
    <section className="panel matura-summary">
      <div><p className="eyebrow">TWOJA MATURA → TWOJE KIERUNKI</p><h2>Kierunki dopasowane do mojej matury</h2>
        <p>{selected.length ? `Twoje rozszerzenia: ${selected.join(', ')}. Wyniki: ${known} z ${selected.length}.` : 'Zaznacz rozszerzenia w profilu, aby ułożyć osobisty ranking. Dodaj wyniki PP i PR, aby obliczyć punkty.'}</p>
        <button onClick={editProfile}>Edytuj mój profil</button>
      </div>
      <div className="matura-summary-count"><strong>{results.filter(r => r.reachesThreshold).length}</strong><span>ofert z osiągniętym co najmniej jednym porównywalnym progiem 2026/27</span></div>
    </section>
    <details className="panel matura-method"><summary>Jak ustalamy kolejność i porównujemy progi?</summary>
      <p>Dopasowanie to udział maksymalnych punktów za rozszerzenia, jaki dałby Twój zestaw przedmiotów przy wyniku 100% z każdego z nich. Uwzględniamy wagi, alternatywy i zakazy ponownego użycia przedmiotu z rzeczywistego wzoru uczelni. Dwa przedmioty w jednej puli wyboru nie dają podwójnej premii. Wyniki PP, Twoje rzeczywiste procenty i egzaminy dodatkowe wpływają na kalkulator punktów, a nie na kolejność. Remisy rozstrzyga nazwa kierunku, następnie identyfikator oferty. Wartości zaokrąglamy tylko na ekranie.</p>
      <p>100% dopasowania oznacza pełne pokrycie punktowanych rozszerzeń, nie szansę przyjęcia. Brak kalkulatora oznacza brak oceny dopasowania; taka oferta jest na końcu listy. Brak wpisanego wyniku nie jest zerem.</p>
      <p>Ubiegły nabór względem planowanego startu 2027/28 to {MATCHING_HISTORY_YEAR}. Różnicę liczymy według osobnych zasad tego naboru, wyłącznie dla oficjalnego progu. Filtr wymaga osiągnięcia przynajmniej jednego takiego progu oraz spełnienia warunków objętych obecnym i historycznym kalkulatorem. Pokazujemy wszystkie opublikowane ustalenia, również sprzeczne; żaden próg nie jest wybierany po cichu.</p>
      <p>Porównanie historyczne jest obecnie dostępne dla Uniwersytetu Ekonomicznego we Wrocławiu. Pozostałe uczelnie mają jawny brak potwierdzonego wzoru historycznego. Dane portali pozostają informacją orientacyjną. Nie przenosimy progów między latami, językami ani kierunkami. Osiągnięcie progu nie gwarantuje przyjęcia w kolejnym naborze; dokumenty, język, uprawnienia i pozostałe warunki sprawdź w karcie kierunku.</p>
    </details>
    <section className="panel matura-filters" aria-label="Filtry dopasowania">
      <label>Szukaj kierunku<input type="search" value={query} onChange={e => { setQuery(e.target.value); setAll(false); }}/></label>
      <label>Uczelnia<select value={university} onChange={e => { setUniversity(e.target.value); setAll(false); }}><option value="">Wszystkie uczelnie</option>{catalogue.universities.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}</select></label>
      <label>Język studiów<select value={language} onChange={e => { setLanguage(e.target.value); setAll(false); }}><option value="">Każdy język</option><option value="pl">Polski</option><option value="en">Angielski</option></select></label>
      <label className="matura-check"><input type="checkbox" checked={matchedOnly} onChange={e => { setMatchedOnly(e.target.checked); setAll(false); }}/>Tylko kierunki premiujące moje rozszerzenia</label>
      <label className="matura-check"><input type="checkbox" checked={reachedOnly} onChange={e => { setReachedOnly(e.target.checked); setAll(false); }}/>Osiągam próg 2026/27 i warunki kalkulatora</label>
    </section>
    <p role="status">Wyniki: <strong>{filtered.length}</strong> z {results.length} ofert · od największego dopasowania rozszerzeń. Filtr progu obejmuje co najmniej jedno opublikowane ustalenie.</p>
    {!selected.length && <p className="history-warning">Nie wybrano rozszerzeń. Kolejność znanych reguł jest na razie alfabetyczna.</p>}
    {!filtered.length && <section className="panel"><h3>Brak ofert spełniających te filtry</h3><p>To może oznaczać niepełne wyniki lub brak porównywalnego progu, a nie brak możliwości studiowania. Uzupełnij profil albo wyłącz filtr progu.</p><button onClick={() => { setQuery(''); setUniversity(''); setLanguage(''); setMatchedOnly(false); setReachedOnly(false); }}>Wyczyść filtry</button></section>}
    <ol className="matura-results">{visible.map(result => {
      const { programme: p, rule, fit, score } = result;
      return <li className="panel matura-result" key={p.id} data-matura-programme={p.id}>
        <header><div><p className="muted">{catalogue.universities.find(u => u.id === p.universityId)?.name} · {p.language === 'pl' ? 'po polsku' : 'po angielsku'}</p><h3><button className="title-button" onClick={event => open(p.id, event.currentTarget)}>{p.name} ↗</button></h3></div><div className="matura-fit"><strong>{fit ? `${number(fit.ratio * 100)}%` : '—'}</strong><span>{fit ? 'dopasowania rozszerzeń' : 'brak reguły punktowej'}</span></div></header>
        <p><strong>Premiowane rozszerzenia z profilu: </strong>{fit?.rewarded.length ? fit.rewarded.join(', ') : 'brak potwierdzonej premii w tej regule'}</p>
        {fit && <details><summary>Wagi Twoich rozszerzeń we wzorze</summary><p>Najlepszy wariant zestawu przy 100% PR (przy remisie pokazujemy jeden wariant; przedmioty alternatywne nie sumują się):</p><ul>{fit.rows.map((r, i) => <li key={i}>{r.label}: {r.subject} — {number(r.value!)} pkt przy 100% PR.</li>)}</ul><p className="muted">Łącznie {number(fit.points)} z {number(fit.capacity)} możliwych punktów za PR. To symulacja zestawu przedmiotów; Twój wynik widnieje niżej.</p></details>}
        <div className="matura-score"><div><span>Twoje punkty · {rule?.year ?? 'brak reguły'}</span><strong>{score?.total !== null && score?.total !== undefined ? `${number(score.total)} pkt` : 'Brak pełnego wyniku'}</strong></div><p>{!rule ? 'Procedura wymaga odrębnej oceny dokumentów.' : score?.status === 'requirement' ? 'Wpisane wyniki nie spełniają warunków kalkulatora.' : score?.status === 'missing' ? 'Uzupełnij wyniki lub dodatkowy etap w karcie kierunku.' : 'Warunki objęte kalkulatorem spełnione. Pozostałe wymagania sprawdź w karcie.'}</p></div>
        {score && <details><summary>Sprawdź obliczenie i ograniczenia</summary><ul>{score.rows.map((r, i) => <li key={i}>{r.label}: {r.detail} {r.value !== null ? `= ${number(r.value)} pkt` : ''}</li>)}{score.issues.map((issue, i) => <li key={`issue-${i}`}>{issue}</li>)}</ul><p>{rule?.caveat}</p></details>}
        <section className="matura-history"><h4>Progi z ubiegłego naboru · {MATCHING_HISTORY_YEAR}</h4>
          {result.historicalRule && <p>Twój wynik według zasad {MATCHING_HISTORY_YEAR}: <strong>{result.historicalScore?.total === null ? 'brak pełnego wyniku' : `${number(result.historicalScore!.total!)} pkt`}</strong>. {result.historicalScore?.status === 'requirement' && 'Warunki tego kalkulatora niespełnione.'}</p>}
          {!result.thresholds.length && <p className="muted">Brak progu z tego naboru w bazie. Starszą historię znajdziesz w karcie kierunku.</p>}
          {result.thresholds.map(({ threshold: t, delta, reason }, i) => {
            const source = catalogue.sources.find(s => s.id === t.sourceId);
            return <div className="matura-threshold" key={i}><p><strong>{number(t.value)} pkt</strong> · {t.round ? `Tura / ustalenie: ${t.round}` : 'Tura niepodana'} · {t.status === 'official' ? 'Publikacja uczelni' : 'Źródło zewnętrzne'} · {t.basis === 'admission' ? 'przyjęcie' : t.basis === 'qualification' ? 'kwalifikacja' : 'definicja progu niepotwierdzona'}</p>
              {delta !== null ? <p className={delta >= -1e-9 ? 'matura-reached' : ''}>Twój wynik historyczny − próg: <strong>{delta >= 0 ? '+' : ''}{number(delta)} pkt</strong> · {delta >= -1e-9 ? 'osiągasz ten próg' : 'poniżej tego progu'}</p> : <p className="muted">Brak porównywalnego wyniku: {reason}</p>}
              <details><summary>Źródło i uwagi o progu</summary><p>{t.note}</p>{source && <p>{sourceExclusion(source.url, 'history') ? source.title : <a href={source.url} target="_blank" rel="noreferrer">{source.title} ↗</a>} · sprawdzono {source.checkedAt}</p>}</details>
            </div>;
          })}
        </section>
      </li>;
    })}</ol>
    {!all && filtered.length > visible.length && <button onClick={() => setAll(true)}>Pokaż wszystkie {filtered.length} ofert</button>}
    <p className="muted">Punkty różnych uczelni mają różne skale. Nie porównujemy ich liczbowo między uczelniami. Ranking korzysta ze wspólnej miary dopasowania zestawu rozszerzeń.</p>
  </section>;
}
