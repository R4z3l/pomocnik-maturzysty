import { programmeDescriptions } from './descriptions';
import { catalogue } from './catalogue';
import { curricula } from './curricula';
import { sourceExclusion } from './sources';
import type { Programme } from './types';
import './programme-description.css';

export default function ProgrammeDescriptionPanel({programme}:{programme:Programme}) {
  const record=programmeDescriptions.find(r=>r.programmeId===programme.id);
  if(!record)return <section><h3>Opis kierunku</h3><p>{programme.description}</p><p className="muted">Rozbudowany opis nie jest jeszcze dostępny w tej wersji bazy.</p></section>;
  const university=catalogue.universities.find(u=>u.id===programme.universityId)!;
  const curriculum=curricula.find(r=>r.programmeId===programme.id);
  const courseNames=[...new Set(curriculum?.groups.flatMap(g=>g.subjects)??[])].filter(s=>!/^(BHP|przysposobienie biblioteczne|wychowanie fizyczne|język (obcy|angielski|polski))/i.test(s)).slice(0,8);
  const sections=[
    {title:'Tematy opisane przez uczelnię',items:record.topics,empty:'W odczytanym opisie nie wyodrębniono dodatkowej listy tematów.'},
    {title:'Jak wygląda nauka',items:record.teachingForms,empty:'Brak potwierdzonego opisu form zajęć na tej karcie źródłowej.'},
    {title:'Praktyki i doświadczenie',items:record.practice,empty:'Nie potwierdzono szczegółów praktyk w opisie. Sprawdź program i regulamin praktyk właściwego cyklu.'},
    {title:'Możliwe obszary pracy według uczelni',items:record.careerAreas,empty:'Brak odrębnej potwierdzonej listy obszarów pracy w tym opisie.'},
  ];
  return <article className="programme-description" aria-label="Opis kierunku na podstawie źródeł uczelni">
    <header><p className="eyebrow">POZNAJ KIERUNEK</p><h3>O czym są te studia?</h3><p className="muted">{university.name} · {programme.language==='en'?'studia po angielsku':'studia po polsku'} · {programme.level==='long-cycle'?'jednolite studia magisterskie':'I stopień'}</p></header>
    <p className="description-editorial-note">Opracowanie na podstawie materiałów uczelni. Krótkie streszczenie i informacje programowe uzupełnia odnośnik do pełnego opisu.</p>
    {record.overview.map((p,i)=><p className="description-overview" key={i}>{p}</p>)}
    {record.status==='limited-source'&&<p className="history-warning">Zakres źródła jest ograniczony. Poniżej zachowujemy wyłącznie informacje potwierdzone w dostępnym materiale; brak szczegółu nie oznacza braku takiej możliwości.</p>}
    <div className="description-sections">{sections.map(section=><section key={section.title}><h4>{section.title}</h4>{section.items.length?<ul>{section.items.map((item,i)=><li key={i}>{item}</li>)}</ul>:<p className="muted">{section.empty}</p>}</section>)}</div>
    {!!record.careerRoles.length&&<section><h4>Przykładowe role wskazane przez uczelnię</h4><div className="tags">{record.careerRoles.map(role=><span className="tag" key={role}>{role}</span>)}</div></section>}
    {!!record.specializations.length&&<section><h4>Ścieżki i specjalności wymienione w opisie</h4><ul>{record.specializations.map(name=><li key={name}>{name}</li>)}</ul><p className="muted">To informacje z karty opisowej. Dostępność ścieżek, zasady ich uruchomienia i zgodność z Twoim cyklem sprawdź w dokumentach uczelni. Status zweryfikowanego programu pozostaje w zakładce „Program i specjalności”.</p></section>}
    {!!record.careerAreas.length&&<p className="muted">To wskazane przez uczelnię możliwości, nie pomiar zatrudnienia, oferta pracy ani gwarancja uprawnień zawodowych. Dane ELA i analizę rynku pracy sprawdzisz w osobnych zakładkach.</p>}
    {!!courseNames.length&&<section className="description-courses"><h4>Przykłady zajęć w opublikowanym programie</h4><div className="tags">{courseNames.map(name=><span className="tag" key={name}>{name}</span>)}</div><p className="muted">Cykl programu: {curriculum?.referenceYear} · {curriculum?.completeness==='full-plan'?'pełny opublikowany spis':'spis częściowy'}. To przykłady, nie cały plan. Całą zebraną listę znajdziesz w „Program i specjalności”.</p></section>}
    <aside className="description-source"><h4>Opis uczelni i pochodzenie danych</h4>
      <p>{sourceExclusion(record.sourceUrl)?<span>{record.sourceTitle} — źródło wykluczone z bieżącego odczytu</span>:<a href={record.sourceUrl} target="_blank" rel="noreferrer">{record.status==='limited-source'?'Otwórz kartę kierunku na stronie uczelni':'Przeczytaj pełny opis na stronie uczelni'} ↗</a>}</p>
      <p className="muted">Materiał odniesienia: {record.referenceYear} · odczyt {record.checkedAt}. Ogólny opis nie potwierdza uruchomienia oferty ani niezmienionego programu na 2027/28.</p>
      {!!record.sourceSections.length&&<details><summary>Sekcje dostępne w materiale źródłowym ({record.sourceSections.length})</summary><ul>{record.sourceSections.map((name,i)=><li key={i}>{name}</li>)}</ul></details>}
      {record.notes.map((note,i)=><p className="muted" key={i}>{note}</p>)}
    </aside>
  </article>;
}
