import { useState, type ReactNode } from 'react';
import update from '../docs/aktualizacja-ai.md?raw';
import university from '../docs/dodawanie-uczelni.md?raw';
import sources from '../docs/hierarchia-zrodel.md?raw';
import curriculum from '../docs/przedmioty-i-specjalnosci.md?raw';
import publishing from '../docs/publikacja-prywatna.md?raw';
import universityCards from '../docs/fiszki-uczelni.md?raw';
import pwrAudit from '../docs/audyt-pwr.md?raw';
import dataRefresh from '../docs/aktualizacja-bez-ai.md?raw';
import './instructions.css';

// Instrukcje są włączane podczas budowania aplikacji. Nowe instrukcje dodaj tutaj.
const instructions = [
  { id: 'baza', title: 'Aktualizacja bazy bez AI', text: dataRefresh },
  { id: 'fiszki', title: 'Uczelnie — fiszki i przegląd', text: universityCards },
  { id: 'politechnika', title: 'Politechnika Wrocławska — zakres danych', text: pwrAudit },
  { id: 'aktualizacja', title: 'Aktualizacja z pomocą AI', text: update },
  { id: 'uczelnia', title: 'Dodawanie uczelni', text: university },
  { id: 'zrodla', title: 'Zasady i hierarchia źródeł', text: sources },
  { id: 'programy', title: 'Przedmioty i specjalności', text: curriculum },
  { id: 'publikacja', title: 'Prywatna wersja online', text: publishing },
];

function inline(value: string): ReactNode[] {
  const pattern = /(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\(https?:\/\/[^\s)]+\))/g;
  return value.split(pattern).filter(Boolean).map((part, index) => {
    if (part.startsWith('**')) return <strong key={index}>{part.slice(2, -2)}</strong>;
    if (part.startsWith('`')) return <code key={index}>{part.slice(1, -1)}</code>;
    const link = part.match(/^\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)$/);
    if (link) return <a key={index} href={link[2]} target="_blank" rel="noreferrer">{link[1]} ↗</a>;
    return part;
  });
}

function Markdown({ text }: { text: string }) {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const nodes: ReactNode[] = [];
  let index = 0;
  const special = (line: string) => /^(#{1,4} |```|> |[-*] |\d+\. |---\s*$)/.test(line);
  while (index < lines.length) {
    const line = lines[index];
    if (!line.trim()) { index++; continue; }
    const key = index;
    if (line.startsWith('```')) {
      const content: string[] = []; index++;
      while (index < lines.length && !lines[index].startsWith('```')) content.push(lines[index++]);
      if (index < lines.length) index++;
      nodes.push(<pre key={key}><code>{content.join('\n')}</code></pre>); continue;
    }
    const heading = line.match(/^(#{1,4})\s+(.+)$/);
    if (heading) { const contents = inline(heading[2]); nodes.push(heading[1].length === 1 ? <h2 key={key}>{contents}</h2> : heading[1].length === 2 ? <h3 key={key}>{contents}</h3> : <h4 key={key}>{contents}</h4>); index++; continue; }
    if (/^---\s*$/.test(line)) { nodes.push(<hr key={key}/>); index++; continue; }
    if (/^> /.test(line)) { const quote: string[] = []; while (index < lines.length && /^> /.test(lines[index])) quote.push(lines[index++].slice(2)); nodes.push(<blockquote key={key}>{inline(quote.join(' '))}</blockquote>); continue; }
    if (/^[-*] |^\d+\. /.test(line)) {
      const ordered = /^\d+\. /.test(line); const items: string[] = [];
      while (index < lines.length && (ordered ? /^\d+\. / : /^[-*] /).test(lines[index])) items.push(lines[index++].replace(ordered ? /^\d+\. / : /^[-*] /, ''));
      const contents = items.map((item, i) => <li key={i}>{inline(item)}</li>);
      nodes.push(ordered ? <ol key={key}>{contents}</ol> : <ul key={key}>{contents}</ul>); continue;
    }
    const paragraph: string[] = [];
    while (index < lines.length && lines[index].trim() && !special(lines[index])) paragraph.push(lines[index++]);
    nodes.push(<p key={key}>{inline(paragraph.join(' '))}</p>);
  }
  return <>{nodes}</>;
}

export default function InstructionsPanel() {
  const [selected, setSelected] = useState(instructions[0].id);
  const [feedback, setFeedback] = useState('');
  const item = instructions.find(instruction => instruction.id === selected)!;
  const prompt = item.id === 'aktualizacja' ? item.text.split('\n').filter(line => line.startsWith('> ')).map(line => line.slice(2)).join('\n\n') : '';
  async function copyPrompt() {
    try { await navigator.clipboard.writeText(prompt); setFeedback('Polecenie skopiowane.'); }
    catch { setFeedback('Nie udało się skopiować. Możesz zaznaczyć polecenie poniżej i skopiować je ręcznie.'); }
  }
  return <section className="instructions-layout" aria-label="Instrukcje">
    <nav className="panel instructions-menu" aria-label="Wybierz instrukcję"><h2>Instrukcje</h2><p>Wybierz temat, który chcesz przeczytać.</p>{instructions.map(instruction => <button key={instruction.id} aria-pressed={selected === instruction.id} onClick={() => { setSelected(instruction.id); setFeedback(''); }}>{instruction.title}</button>)}</nav>
    <article className="panel instructions-document" aria-label={item.title}>{prompt && <div className="instructions-copy"><button onClick={copyPrompt}>Kopiuj polecenie dla AI</button><span role="status">{feedback}</span></div>}<Markdown text={item.text}/></article>
  </section>;
}
