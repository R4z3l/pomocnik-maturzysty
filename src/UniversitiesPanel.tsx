import { useState, type ReactNode } from 'react';
import { catalogue } from './catalogue';
import './universities.css';

export default function UniversitiesPanel({ browse, sources }: {
  browse: (universityId: string) => void;
  sources: (ids: string[]) => ReactNode;
}) {
  const [query, setQuery] = useState('');
  const normalize = (text: string) => text.toLocaleLowerCase('pl').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ł/g, 'l');
  const universities = catalogue.universities.filter(u => normalize(`${u.name} ${u.shortName}`).includes(normalize(query.trim())));
  return <div className="universities-page">
    <section className="university-overview" aria-label="Uczelnie w liczbach">
      <div><p className="eyebrow">TWÓJ AKADEMICKI PUNKT STARTU</p><h2>Najpierw uczelnia.<br/>Potem Twoja ścieżka.</h2><p>Zobacz, co już znajdziesz w aplikacji i jaki zakres oferty obejmują zebrane dane.</p></div>
      <dl><div><dt>Uczelnie w systemie</dt><dd>{catalogue.universities.length}</dd></div><div><dt>Oferty studiów</dt><dd>{catalogue.programmes.length}</dd></div><div><dt>Miasta w katalogu</dt><dd>{new Set(catalogue.programmes.map(p => p.city)).size}</dd></div></dl>
    </section>
    <div className="university-toolbar"><div><h2>Uczelnie w Twoim atlasie</h2><p>Fiszki opisują zakres aplikacji, nie pełną ofertę uczelni.</p></div><label><span className="sr-only">Szukaj uczelni</span><input type="search" placeholder="Szukaj uczelni…" value={query} onChange={e => setQuery(e.target.value)}/></label></div>
    <p className="muted" role="status">Widoczne uczelnie: {universities.length} z {catalogue.universities.length}</p>
    <section className="university-grid" aria-label="Fiszki uczelni">
      {universities.map((u, index) => {
        const offers = catalogue.programmes.filter(p => p.universityId === u.id);
        const fields = [...new Set(offers.flatMap(p => p.fields))].sort((a, b) => a.localeCompare(b, 'pl'));
        const polish = offers.filter(p => p.language === 'pl').length;
        const bachelor = offers.filter(p => p.level === 'bachelor').length;
        const cities = [...new Set(offers.map(p => p.city))];
        return <article className="university-sheet" key={u.id} aria-labelledby={`university-${u.id}`}>
          <header className={`university-sheet-header university-accent-${index % 2}`}><span className="university-sheet-number" aria-hidden="true">{String(catalogue.universities.indexOf(u) + 1).padStart(2, '0')} / UCZELNIA</span><span className="university-sheet-badge">W katalogu</span><h2 id={`university-${u.id}`}>{u.name}</h2><p>{cities.length ? cities.join(' · ') : 'Lokalizacja nieuzupełniona'} · Stacjonarne</p></header>
          <div className="university-sheet-body">
            <div className="university-offer-total"><strong>{offers.length}</strong><span>ofert studiów<br/>w aplikacji</span><button className="primary-button" onClick={() => browse(u.id)}>Zobacz kierunki ↗<span className="sr-only"> — {u.name}</span></button></div>
            <dl className="university-facts"><div><dt>Język studiów · liczba ofert</dt><dd>Polski: {polish} · Angielski: {offers.length - polish}</dd></div><div><dt>Poziom · liczba ofert</dt><dd>I stopień: {bachelor} · Jednolite magisterskie: {offers.length - bachelor}</dd></div><div><dt>Roczniki odniesienia ofert</dt><dd>{[...new Set(offers.map(p => p.referenceYear))].sort().join(' · ') || 'Brak ofert'}</dd></div></dl>
            <section className="university-fields"><h3>Obszary, które możesz odkryć</h3><div className="tags">{fields.slice(0, 8).map(field => <span className="tag" key={field}>{field}</span>)}</div>{fields.length > 8 && <details><summary>Pozostałe obszary ({fields.length - 8})</summary><div className="tags">{fields.slice(8).map(field => <span className="tag" key={field}>{field}</span>)}</div></details>}{!fields.length && <p className="muted">Brak opisanych obszarów.</p>}</section>
            <section className="university-scope"><h3>Co obejmują dane?</h3><p>{u.coverage}</p></section>
            <details className="university-evidence"><summary>Źródła i daty sprawdzenia</summary>{sources(u.sourceIds)}</details>
          </div>
        </article>;
      })}
      {!universities.length && <div className="empty-state"><h2>Nie ma takiej uczelni w katalogu.</h2><p>Spróbuj pełnej nazwy lub skrótu uczelni.</p><button onClick={() => setQuery('')}>Pokaż wszystkie uczelnie</button></div>}
    </section>
    <aside className="university-footnote"><strong>Nie widzisz wybranej uczelni?</strong><p>Ten katalog obejmuje wybrane uczelnie i oferty. Brak uczelni oznacza brak jej danych w systemie. Liczby dotyczą ofert: wersje językowe tego samego kierunku mogą być osobnymi pozycjami.</p></aside>
  </div>;
}
