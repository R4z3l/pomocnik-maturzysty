import { useState } from 'react';
import type { Programme, Profile } from './types';
import { families, suggestedFamilies, preferenceNotes, evidence, expertOpinions, analysisDate } from './careers';
import jobs from './data/jobs.json';
import { jobSearchLinks } from './jobSearch';
import { displayJobStatus, localDate } from './jobStatus';
import './advisor.css';

type Props = { programme: Programme; profile: Profile; update: (profile: Profile) => void };
const levelNames: Record<string, string> = { internship: 'Staż / praktyka', entry: 'Wejście do zawodu', experienced: 'Z doświadczeniem', unknown: 'Poziom nieustalony' };
const statusNames: Record<string, string> = { confirmed: 'Aktywność potwierdzona w dniu sprawdzenia', unconfirmed: 'Aktywność niepotwierdzona', expired: 'Archiwalna lub minął zapisany termin' };
function daysSince(date: string) { return Math.floor((Date.now() - Date.parse(`${date}T00:00:00`)) / 86_400_000); }
function EvidenceLink({ id }: { id: string }) {
  const item = evidence.find(e => e.id === id);
  return item ? <a href={item.url} target="_blank" rel="noreferrer">{item.title} ↗</a> : <span>Brak wpisu źródłowego: {id}</span>;
}

export default function CareerPanel({ programme, profile, update }: Props) {
  const [showArchive, setShowArchive] = useState(false);
  const suggested = suggestedFamilies(programme);
  const choice = profile.careerChoices?.[programme.id];
  const family = families.find(f => f.id === choice) ?? suggested[0];
  if (!family) return <section className="career-advisor" aria-label="Ścieżki zawodowe i rynek pracy">
    <h3>Brak dopasowanej analizy rodziny zawodów</h3>
    <p>Nie opracowano jeszcze analizy rynku pracy odpowiadającej temu kierunkowi. Nie przypisujemy mu automatycznie danych innej branży. Przykładowe obszary pracy powyżej wynikają z programu studiów.</p>
    <label className="advisor-family-label">Rozważana rodzina zawodów<select value="" onChange={event => update({ ...profile, careerChoices: { ...profile.careerChoices, [programme.id]: event.target.value } })}>
      <option value="" disabled>Wybierz samodzielnie, jeśli chcesz zbadać inną ścieżkę</option>
      {families.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
    </select></label><p className="muted">Ręczny wybór rodziny nie potwierdza zgodności z kierunkiem ani uprawnień zawodowych.</p>
  </section>;
  const today = localDate(new Date());
  const familyJobs = jobs.jobs.filter(job => job.familyId === family.id).map(job => ({ ...job, active: displayJobStatus(job, today) }));
  const visibleJobs = familyJobs.filter(job => showArchive || job.active !== 'expired');
  const confirmed = familyJobs.filter(job => job.active === 'confirmed');
  const unconfirmed = familyJobs.filter(job => job.active === 'unconfirmed');
  const archive = familyJobs.filter(job => job.active === 'expired');
  const relevantSourceIds = new Set(familyJobs.map(job => job.sourceId));
  const relevantSources = jobs.sources.filter(source => relevantSourceIds.has(source.id));
  const notes = preferenceNotes(profile, family);
  const staleJobs = familyJobs.some(job => daysSince(job.checkedAt) > 14);
  const staleAnalysis = daysSince(analysisDate) > 90;

  return <section className="career-advisor" aria-label="Ścieżki zawodowe i rynek pracy">
    <div className="advisor-heading"><p className="advisor-kicker">OD KIERUNKU DO ZAWODU</p><h3>Sprawdź możliwą drogę</h3><p>To rodziny zawodów i hipotezy przejścia ze studiów do pracy. Powiązanie nie potwierdza kwalifikacji ani uprawnień wynikających z tego programu.</p></div>
    <label className="advisor-family-label">Rozważana rodzina zawodów<select value={family.id} onChange={event => update({ ...profile, careerChoices: { ...profile.careerChoices, [programme.id]: event.target.value } })}>
      {suggested.length > 0 && <optgroup label="Sugerowane na podstawie nazwy i opisu kierunku">{suggested.map(f => <option key={f.id} value={f.id}>{f.name}</option>)}</optgroup>}
      <optgroup label="Pozostałe rodziny — możesz wybrać inną">{families.filter(f => !suggested.some(s => s.id === f.id)).map(f => <option key={f.id} value={f.id}>{f.name}</option>)}</optgroup>
    </select></label>
    {!choice && <div className="advisor-callout">Wyświetlamy propozycję do sprawdzenia. <button className="text-button" onClick={() => update({ ...profile, careerChoices: { ...profile.careerChoices, [programme.id]: family.id } })}>Zapisz tę rodzinę w profilu</button></div>}
    <p className="advisor-caption">{choice ? 'Wybór rodziny jest częścią profilu. Zachowaj go przyciskiem „Zapisz profil”.' : 'Sugestia opiera się na słowach kluczowych, bez automatycznej oceny predyspozycji.'}</p>
    <div className="advisor-role-list">{family.roles.map(role => <span key={role}>{role}</span>)}</div>
    <p>{family.entry}</p>
    <details className="advisor-details" open><summary>Dopasowanie do Twoich preferencji</summary><ul className="advisor-notes">{notes.map(text => <li key={text}>{text}</li>)}</ul><p className="advisor-caption">{family.mobility} Te wskazówki nie są oceną kompetencji ani wynikiem rekrutacji.</p></details>
    <details className="advisor-details"><summary>Umiejętności i droga do zawodu</summary><p className="advisor-caption">Przykładowe umiejętności do zweryfikowania w sylabusie i ogłoszeniach:</p><div className="advisor-role-list">{family.skills.map(skill => <span key={skill}>{skill}</span>)}</div><ol className="advisor-timeline">{family.path.map((step, index) => <li key={step.stage}><span className="advisor-step-number">{index + 1}</span><div><strong>{step.stage}</strong><span className="advisor-step-duration">{step.duration}</span><span className={`advisor-badge ${step.kind === 'Wymóg formalny' ? 'advisor-badge-amber' : ''}`}>{step.kind}</span><p>{step.note}</p></div></li>)}</ol><div className="advisor-callout"><strong>Koszty: nieustalone.</strong> Brak kwot nie oznacza bezpłatnej ścieżki. Zweryfikuj opłaty, praktyki i wymagania dla konkretnego zawodu oraz roku uzyskiwania kwalifikacji.</div></details>

    <details className="advisor-details"><summary>Perspektywy na 5, 10 i 15 lat</summary><p className="advisor-caption">Analiza: {analysisDate}. Horyzont liczony od analizy, a nie od rozpoczęcia studiów. Pewność niska; nie przewidujemy wynagrodzeń ani prawdopodobieństwa zatrudnienia.</p>{staleAnalysis && <p className="advisor-warning" role="status">Analiza ma ponad 90 dni. Przed decyzją należy odświeżyć źródła i założenia.</p>}
      <div className="advisor-layer"><span className="advisor-kicker">1 / DANE I GRANICE ŹRÓDEŁ</span>{family.evidenceIds.map(id => { const item = evidence.find(e => e.id === id); return item ? <article className="advisor-evidence" key={id}><EvidenceLink id={id}/><small>{item.date} · {item.scope}</small><p>{item.finding}</p></article> : null; })}</div>
      <details className="advisor-experts"><summary>2 / Eksperci — wspólny kontekst metody i AI</summary><p className="advisor-caption">Poniższe wypowiedzi dotyczą badania ILO–NASK i wpływu AI na zadania. Nie są prognozami zatrudnienia w tej konkretnej rodzinie. Nie zebrano tu odrębnego panelu ekspertów dla wybranego zawodu.</p>{expertOpinions.map(opinion => <article key={opinion.name}><strong>{opinion.name}</strong><small>{opinion.role}</small><p>{opinion.text}</p><EvidenceLink id={opinion.sourceId}/></article>)}</details>
      <div className="advisor-layer"><span className="advisor-kicker">3 / WŁASNA SYNTEZA AI · SCENARIUSZE</span><p className="advisor-caption">Interpretacja materiałów, nie cytat z prognozy. Raporty mają różne zakresy: WEF do 2030, Cedefop do 2035; ILO opisuje ekspozycję zadań. Lata 2036 i 2041 wykraczają poza prognozę Cedefop.</p><div className="advisor-horizons">{family.outlook.map((outlook, index) => <article key={index}><div><strong>+{[5, 10, 15][index]} lat</strong><span>{[2031, 2036, 2041][index]}</span></div><p>{outlook}</p><small>{index === 0 ? 'Około 4 lat od startu studiów w 2027; część osób nadal w trakcie kształcenia.' : index === 1 ? 'Około 9 lat od startu studiów; etap kariery zależy od ścieżki i dalszej nauki. Scenariusz poza prognozą do 2035.' : 'Około 14 lat od startu studiów. Scenariusz poza prognozą do 2035, z dużą niepewnością.'}</small></article>)}</div><div className="advisor-scenario"><strong>Szansa / korzystny kierunek działania</strong><p>{family.opportunity}</p></div><div className="advisor-scenario advisor-risk"><strong>Ryzyko do uwzględnienia</strong><p>{family.risk}</p></div></div>
    </details>


    <details className="advisor-details advisor-market" open><summary>Rynek pracy — ostatnie uzupełnienie {jobs.checkedAt}</summary><p className="advisor-caption">{jobs.scopeNote}</p>{staleJobs && <p className="advisor-warning" role="status">Niektóre ogłoszenia sprawdzono ponad 14 dni temu. Sprawdź datę przy każdym ogłoszeniu i jego aktualność u źródła.</p>}
      <div className="advisor-callout"><strong>Sprawdź nowsze oferty we Wrocławiu</strong><p className="advisor-caption">Otwórz przykładowe wyszukiwanie i dostosuj hasło, lokalizację oraz filtry na portalu. Wyniki mogą obejmować inne poziomy doświadczenia i stanowiska; sprawdź treść ogłoszenia i datę jego ważności. Serwisy mogą ograniczać dostęp.</p>{jobSearchLinks(family.id).map(search => <p key={search.label}><strong>{search.label}</strong> · hasło „{search.query}”: {search.portals.map((portal, index) => <span key={portal.name}>{index > 0 && ' · '}<a href={portal.url} target="_blank" rel="noreferrer">{portal.name} ↗</a></span>)}</p>)}</div>
      <div className="advisor-market-counts">{(['internship', 'entry', 'experienced'] as const).map(level => <div key={level}><strong>{confirmed.filter(job => job.level === level).length}</strong><span>{levelNames[level]}</span><small>potwierdzone w próbie</small></div>)}</div>
      <p className="advisor-caption">Mianownik: {familyJobs.length} unikalnych ogłoszeń tej rodziny w zapisanej próbie, w tym {confirmed.length} potwierdzonych w dniu ich sprawdzenia, {unconfirmed.length} niepotwierdzonych i {archive.length} archiwalnych lub po zapisanym terminie. Terminy są sprawdzane według daty urządzenia; przedłużenie naboru wymaga ponownego sprawdzenia źródła. Liczymy ogłoszenia, nie liczbę stanowisk. Zera nie dowodzą braku popytu.</p>
      <p className="advisor-caption">Aktualne pokrycie tej próby: {relevantSources.length ? relevantSources.map(source => source.publisher).join('; ') : 'brak zebranych ogłoszeń dla tej rodziny'}. Nie obejmuje całego rynku ani wszystkich pracodawców. Nie ma porównywalnej historii do wyliczenia trendu.</p>
      <label className="advisor-archive"><input type="checkbox" checked={showArchive} onChange={event => setShowArchive(event.target.checked)}/> Pokaż także archiwalne ({archive.length})</label>
      <div className="advisor-job-list">{visibleJobs.length === 0 && <p className="advisor-callout">Brak {showArchive ? 'zapisanych' : 'potwierdzonych lub niepotwierdzonych'} ogłoszeń dla tej rodziny w próbie. To luka w materiale, nie ocena dostępności pracy.</p>}{visibleJobs.map(job => { const source = jobs.sources.find(item => item.id === job.sourceId); return <details className="advisor-job" key={job.id}><summary><span><strong>{job.title}</strong><small>{job.employer} · {job.location}</small><span className={`advisor-badge ${job.active !== 'confirmed' ? 'advisor-badge-amber' : ''}`}>{statusNames[job.active] ?? job.active}</span><span className="advisor-badge">{levelNames[job.level] ?? job.level}</span></span></summary><dl className="advisor-job-dates"><div><dt>Opublikowano</dt><dd>{job.publishedAt ?? 'Nie podano'}</dd></div><div><dt>Ważna do</dt><dd>{job.expiresAt ?? 'Nie podano'}</dd></div><div><dt>Pierwsze / ostatnie wykrycie</dt><dd>{job.firstSeen} / {job.lastSeen}</dd></div><div><dt>Sprawdzono</dt><dd>{job.checkedAt}</dd></div></dl><h4>Wymagania z ogłoszenia</h4>{job.requirements.length ? <ul>{job.requirements.map(requirement => <li key={requirement}>{requirement}</li>)}</ul> : <p>Brak odczytanych wymagań — nie dopowiadamy ich.</p>}<h4>Łączenie ze studiami</h4><p>{job.studyCompatible}</p><h4>Wynagrodzenie z tej oferty</h4><p>{job.salary ?? 'Nie podano kwoty.'}</p><p className="advisor-caption">Kwota dotyczy wyłącznie tego ogłoszenia i wskazanej formy rozliczenia. Nie porównujemy stawek o różnych jednostkach ani formach umowy.</p><h4>Kontekst i pochodzenie</h4><p>{job.note}</p><a href={job.url} target="_blank" rel="noreferrer">Otwórz kartę ogłoszenia ↗</a>{source && <div className="advisor-provenance"><a href={source.url} target="_blank" rel="noreferrer">{source.title} ↗</a><small>{source.publisher} · {source.kind === 'official' ? 'źródło oficjalne' : 'portal'} · sprawdzono {source.checkedAt}</small><p>{source.note}</p></div>}</details>; })}</div>
      {relevantSources.length > 0 && <details className="advisor-market-sources"><summary>Sprawdź nowsze ogłoszenia w źródłach</summary><p className="advisor-caption">To zapisane adresy list źródłowych. Ich zawartość może się zmienić; portal nie pobiera jej automatycznie.</p><ul>{relevantSources.map(source => <li key={source.id}><a href={source.url} target="_blank" rel="noreferrer">{source.title} ↗</a></li>)}</ul></details>}
    </details>
  </section>;
}
