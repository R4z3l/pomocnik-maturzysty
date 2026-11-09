import { useState } from 'react';
import type { Programme } from './types';
import { catalogue } from './catalogue';
import { historyCoverage } from './history';
import {sourcePriority} from './sources';
export default function ThresholdPanel({programme}:{programme:Programme}) {
 const [officialOnly,setOfficialOnly]=useState(false);
 const [year,setYear]=useState('');
 const coverage=historyCoverage(programme.thresholds,catalogue.sources);
 const covered=coverage.filter(y=>y.rows.length).length;
 const officialYears=coverage.filter(y=>y.rows.some(t=>t.status==='official')).length;
 return <section className="history-panel"><h3>Progi historyczne · nabory 2024–2026</h3><p className="muted">Dane dla {covered} z {coverage.length} roczników; publikacje uczelni dla {officialYears}. Liczba rekordów może być większa niż liczba naborów: zachowujemy odrębne źródła, tury i definicje.</p>
 <label className="field-label">Rok historii<select value={year} onChange={e=>setYear(e.target.value)}><option value="">Wszystkie roczniki 2024–2026</option>{coverage.map(y=><option key={y.year}>{y.year}</option>)}</select></label>
 <label className="check-inline"><input type="checkbox" checked={officialOnly} onChange={e=>setOfficialOnly(e.target.checked)}/>Tylko publikacje uczelni</label>
 <p className="muted">Kwalifikacja, przyjęcie i minimum formalne to różne pojęcia. Tura niepodana nie oznacza tury pierwszej. Brak wartości nie oznacza zera ani nieuruchomienia kierunku.</p>
 {coverage.filter(y=>!year||year===y.year).map(y=>{const rows=y.rows.filter(t=>!officialOnly||t.status==='official');return <section className="history-year" key={y.year}><h4>{y.year}</h4>{y.discrepancy&&!officialOnly&&<p className="history-warning">Źródła podają różne wartości. Mogą opisywać inne tury, tryby albo definicje; nie wybieramy jednej i nie uśredniamy. Sprawdź pochodzenie.</p>}{!rows.length&&<p className="muted">{officialOnly&&y.rows.length?'Brak publikacji uczelni; dostępne są informacje zewnętrzne.':'Brak zweryfikowanej wartości w pakiecie dla tego rocznika.'}</p>}{rows.map((t,i)=>{const source=catalogue.sources.find(s=>s.id===t.sourceId);const label=t.status==='official'?'Publikacja uczelni':source?.kind==='press'?'Relacja prasowa':t.status==='anecdote'?'Zestawienie społecznościowe':'Portal zewnętrzny';return <article className="threshold" key={i}><strong>{t.value.toLocaleString('pl',{maximumFractionDigits:3})}<small>pkt</small></strong><div><span className={'tag '+(t.status==='official'?'':'amber')}>{label}</span><p>{t.round?`Tura: ${t.round}`:'Tura niepodana'} · {t.basis==='admission'?'Przyjęcie':t.basis==='qualification'?'Kwalifikacja':'Definicja progu niepotwierdzona'}</p><small>{t.note}</small>{source&&<p className="source-links"><a href={source.url} target="_blank" rel="noreferrer">{source.title} ↗</a><small>Priorytet {sourcePriority(source)} · {source.publisher} · sprawdzono {source.checkedAt}</small></p>}{(t.supportingSourceIds??[]).map(id=>{const extra=catalogue.sources.find(s=>s.id===id);return extra?<p className="source-links" key={id}><small>Tę samą wartość podaje również:</small><a href={extra.url} target="_blank" rel="noreferrer">{extra.title} ↗</a><small>Priorytet {sourcePriority(extra)} · {extra.publisher} · {extra.checkedAt}. Zgodność nie dowodzi niezależności źródeł ani tej samej tury.</small></p>:null;})}</div></article>;})}</section>;})}
 <p className="muted">Historyczne punkty mogą być liczone według innych wzorów niż obecny kalkulator. Nie wyznaczamy na ich podstawie prawdopodobieństwa przyjęcia.</p></section>;
}
