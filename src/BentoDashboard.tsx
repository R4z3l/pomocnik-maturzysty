import './bento-dashboard.css';

type BentoDashboardProps = {
  query: string;
  onQueryChange: (value: string) => void;
  subjects: string[];
  comparisonCount: number;
  onProfile: () => void;
  onCompare: () => void;
  onSearch: () => void;
};

export default function BentoDashboard({ query, onQueryChange, subjects, comparisonCount, onProfile, onCompare, onSearch }: BentoDashboardProps) {
  return <section className="bento-dashboard" aria-label="Twój atlas możliwości">
    <div className="bento-tile bento-search-tile">
      <svg className="bento-contours" viewBox="0 0 450 180" fill="none" aria-hidden="true" focusable="false">
        <path d="M10 180c60-72 103-19 150-61s57-12 91-51 84-4 112-35 63-19 97-48M35 195c62-72 100-15 149-61s53-8 89-47 81-1 110-32 62-18 97-47M64 210c60-71 97-14 145-59s55-7 89-47 82 0 109-32 61-17 94-44M-22 164c61-70 105-19 150-62s58-13 92-52 85-6 115-37 63-20 97-49M-51 149c60-71 103-22 149-64s60-14 94-54 85-7 115-38 64-21 98-49" />
      </svg>
      <svg className="bento-compass" viewBox="0 0 80 80" fill="none" aria-hidden="true" focusable="false">
        <circle cx="40" cy="40" r="25" /><circle cx="40" cy="40" r="3" />
        <path d="M40 5v12m0 46v12M5 40h12m46 0h12M20 20l9 9m22 22 9 9M20 60l9-9m22-22 9-9" />
        <path className="bento-compass-needle" d="m40 17 6 23-6 23-6-23z" />
      </svg>
      <p className="bento-eyebrow">Twój atlas możliwości</p>
      <h1>Znajdź swój kierunek</h1>
      <p className="bento-search-description">Odkryj studia we Wrocławiu. Wybierz swoją drogę.</p>
      <form className="bento-search-form" role="search" onSubmit={event => { event.preventDefault(); onSearch(); }}>
        <label className="bento-search-field">
          <span className="bento-sr-only">Szukaj kierunku</span>
          <svg viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><circle cx="10.5" cy="10.5" r="7" /><path d="m16 16 5 5" /></svg>
          <input type="search" value={query} onChange={event => onQueryChange(event.target.value)} placeholder="Jaki kierunek Cię interesuje?" />
        </label>
        <button className="bento-search-submit" type="submit">Szukaj</button>
      </form>
    </div>

    <section className="bento-tile bento-profile-tile" aria-labelledby="bento-profile-heading">
      <div className="bento-tile-heading">
        <svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><circle cx="16" cy="9" r="5" /><path d="M4 28v-3a12 12 0 0 1 24 0v3z" /></svg>
        <h2 id="bento-profile-heading">Mój profil</h2>
      </div>
      {subjects.length > 0 ? <>
        <p className="bento-tile-caption">Przedmioty maturalne</p>
        <ul className="bento-subjects">{subjects.slice(0, 3).map(subject => <li key={subject}>{subject}</li>)}</ul>
        {subjects.length > 3 && <p className="bento-more-subjects">Pozostałe: {subjects.length - 3}</p>}
      </> : <p className="bento-empty-profile">Dodaj przedmioty maturalne i poznaj swoje możliwości.</p>}
      <button className="bento-tile-action" type="button" onClick={onProfile}>{subjects.length ? 'Otwórz profil' : 'Uzupełnij profil'}<span aria-hidden="true">↗</span></button>
    </section>

    <section className="bento-tile bento-compare-tile" aria-labelledby="bento-compare-heading">
      <div className="bento-tile-heading">
        <svg viewBox="0 0 32 32" fill="none" aria-hidden="true" focusable="false"><rect x="4" y="10" width="18" height="18" rx="3" /><path d="M11 10V7a3 3 0 0 1 3-3h11a3 3 0 0 1 3 3v11a3 3 0 0 1-3 3h-3" /></svg>
        <h2 id="bento-compare-heading">Porównanie</h2>
      </div>
      <svg className="bento-compare-illustration" viewBox="0 0 210 108" fill="none" aria-hidden="true" focusable="false">
        <g transform="rotate(-12 70 55)"><rect x="20" y="15" width="95" height="76" rx="10" /><path d="M36 36h57M36 49h42M36 62h31" /></g>
        <g transform="rotate(6 140 64)"><rect x="92" y="28" width="98" height="74" rx="10" /><path d="M108 48h57M108 61h43M108 74h29" /></g>
      </svg>
      <p className="bento-comparison-count" aria-live="polite"><strong>{comparisonCount}</strong><span>z 4 ofert</span></p>
      <button className="bento-tile-action" type="button" onClick={onCompare}>Porównaj<span aria-hidden="true">↗</span></button>
    </section>
  </section>;
}
