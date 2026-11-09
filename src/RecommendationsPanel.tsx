import { useState } from 'react';
import { catalogue } from './catalogue';
import { curricula } from './curricula';
import { recommend } from './recommendations';
import type { Profile } from './types';
import './recommendations.css';

export default function RecommendationsPanel({ profile, open }: { profile: Profile; open: (id: string, button: HTMLButtonElement) => void }) {
  const [all, setAll] = useState(false);
  const { results, ambiguous } = recommend(catalogue.programmes, curricula, profile);
  return <section className="panel recommendations"><h2>Kierunki do rozważenia</h2>
    <p>Lista porządkuje kierunki według liczby rodzajów znalezionej zgodności: rozszerzenie maturalne, słowa zainteresowań w opisie lub przedmiotach oraz preferowany rodzaj pracy w sugerowanej rodzinie zawodów. Każdy rodzaj liczymy najwyżej raz. Remisy są alfabetyczne.</p>
    <p className="muted">To proste porównanie słów i zapisanych kategorii, nie analiza AI ani ocena predyspozycji. Odmiany wyrazów, synonimy i kontekst mogą nie zostać rozpoznane; brak zgodności nie oznacza niedopasowania. Przy niepełnych danych mniejsza liczba wskazówek nie oznacza gorszego kierunku. Pole stylu pracy, wyniki matur, dodatkowe wymagania, warunki lokalizacji i indywidualne kwalifikacje nie wpływają na tę kolejność: sprawdź je osobno w karcie kierunku. Kolejność nie jest oceną szans przyjęcia.</p>
    {ambiguous && <p role="status">W zainteresowaniach wykryto zaprzeczenie. Aby nie odwrócić znaczenia wypowiedzi, pominięto porównanie słów; pozostałe informacje nadal można wykorzystać.</p>}
    {!results.length ? <p>Nie znaleziono jeszcze zgodności. W profilu zaznacz rozszerzenia, wpisz zainteresowania lub wybierz preferowany rodzaj pracy. Kierunki nadal znajdziesz w katalogu.</p> : <><p>Znaleziono {results.length} ofert z co najmniej jedną wskazówką. Oferty bez wskazówki pozostają w katalogu.</p><ol>{(all ? results : results.slice(0, 12)).map(result => <li key={result.programme.id} className="recommendation-item"><h3><button className="title-button" onClick={event => open(result.programme.id, event.currentTarget)}>{result.programme.name} ↗</button></h3><p className="muted">{catalogue.universities.find(u => u.id === result.programme.universityId)?.name} · {result.programme.language === 'en' ? 'studia po angielsku' : 'studia po polsku'} · rodzaje zgodności: {result.evidence} z 3</p><ul>
      {result.subjectMatches.length > 0 && <li>Wybrane rozszerzenia występują wśród punktowanych przedmiotów: {result.subjectMatches.join(', ')}. To nie potwierdza spełnienia zasad rekrutacji.</li>}
      {result.interestMatches.length > 0 && <li>Słowa z zainteresowań występują w nazwie lub opisie kierunku: {result.interestMatches.join(', ')}.</li>}
      {result.courseMatches.length > 0 && <li>Słowa z zainteresowań występują w nazwach zajęć: {result.courseMatches.join(', ')}.</li>}
      {result.taskMatches.length > 0 && <li>Preferowany rodzaj zadań ({result.taskMatches.join(', ')}) występuje w sugerowanych rodzinach zawodów: {result.familyNames.join(', ')}. Powiązanie jest orientacyjne.</li>}
    </ul>{result.gaps.length > 0 && <p className="muted">Do uzupełnienia lub sprawdzenia: {result.gaps.join(' ')}</p>}</li>)}</ol>{results.length > 12 && <button onClick={() => setAll(!all)}>{all ? 'Pokaż mniej' : `Pokaż wszystkie ${results.length} ofert`}</button>}</>}
  </section>;
}
