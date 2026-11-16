import { cp, mkdir, mkdtemp, readFile, readdir, realpath, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { dirname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const project = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const updates = join(project, 'output', 'aktualizacje-ai');
const optionalRoots = ['requirements-data.txt', 'Aktualizuj-baze.cmd', 'Uruchom-aplikacje.cmd'];
const roots = ['src', 'scripts', 'tests', 'public', 'docs', 'AGENTS.md', 'README.md', 'package.json', 'package-lock.json', 'tsconfig.json', 'index.html', ...optionalRoots];
const digest = bytes => createHash('sha256').update(bytes).digest('hex');

async function scan(base) {
  const found = new Map();
  async function walk(path, name) {
    let entries;
    try { entries = await readdir(path, { withFileTypes: true }); }
    catch (e) { if (e.code === 'ENOENT') return; throw e; }
    for (const entry of entries) {
      const next = `${name}/${entry.name}`.replace(/^\//, '');
      const full = join(path, entry.name);
      if (entry.isSymbolicLink()) throw new Error(`Niedozwolony link symboliczny: ${next}`);
      if (entry.isDirectory()) await walk(full, next);
      else if (entry.isFile()) found.set(next, digest(await readFile(full)));
      else throw new Error(`Nieobsługiwany element: ${next}`);
    }
  }
  for (const root of roots) {
    const full = join(base, root);
    if (['src', 'scripts', 'tests', 'public', 'docs'].includes(root)) await walk(full, root);
    else { try { found.set(root, digest(await readFile(full))); } catch (e) { if (e.code !== 'ENOENT') throw e; } }
  }
  return found;
}

function diffJson(before, after) {
  const result = [];
  let truncated = false;
  const short = value => {
    const text = JSON.stringify(value);
    return text === undefined ? '(brak)' : text.length > 180 ? `${text.slice(0, 180)}…` : text;
  };
  function add(path, a, b) {
    if (result.length >= 200) { truncated = true; return; }
    result.push(`  - ${path || '(cały plik)'}: ${short(a)} → ${short(b)}`);
  }
  function walk(a, b, path) {
    if (JSON.stringify(a) === JSON.stringify(b)) return;
    if (a === null || b === null || typeof a !== 'object' || typeof b !== 'object' || Array.isArray(a) !== Array.isArray(b)) return add(path, a, b);
    if (Array.isArray(a) && Array.isArray(b)) {
      const id = ['id', 'programmeId'].find(key => [...a, ...b].every(item => item && typeof item === 'object' && !Array.isArray(item) && typeof item[key] === 'string') && new Set(a.map(item => item[key])).size === a.length && new Set(b.map(item => item[key])).size === b.length);
      if (id && a.length + b.length) {
        const left = new Map(a.map(item => [item[id], item]));
        const right = new Map(b.map(item => [item[id], item]));
        for (const key of new Set([...left.keys(), ...right.keys()])) walk(left.get(key), right.get(key), `${path}[${id}=${key}]`);
      } else if (a.length === b.length && a.length <= 300) {
        a.forEach((item, index) => walk(item, b[index], `${path}[${index}]`));
      } else add(path, a, b);
      return;
    }
    for (const key of new Set([...Object.keys(a), ...Object.keys(b)])) walk(a[key], b[key], path ? `${path}.${key}` : key);
  }
  walk(before, after, '');
  if (truncated) result.push('  - Dalsze zmiany pominięto w podglądzie; konieczny jest pełny przegląd pliku.');
  return result;
}

async function start() {
  await mkdir(updates, { recursive: true });
  const session = await mkdtemp(join(updates, 'aktualizacja-'));
  const baseline = join(session, 'przed');
  const candidate = join(session, 'propozycja');
  await mkdir(baseline);
  for (const root of roots) {
    try { await cp(join(project, root), join(baseline, root), { recursive: true, errorOnExist: true, force: false }); }
    catch (error) { if (error.code !== 'ENOENT' || !optionalRoots.includes(root)) throw error; }
  }
  const manifest = Object.fromEntries(await scan(baseline));
  await writeFile(join(session, 'manifest-przed.json'), JSON.stringify(manifest, null, 2) + '\n', { encoding: 'utf8', flag: 'wx' });
  await cp(baseline, candidate, { recursive: true, errorOnExist: true, force: false });
  console.log(`Utworzono kopię przed zmianami: ${baseline}\nPropozycja do pracy AI: ${candidate}\nFolder aktualizacji: ${session}\nNie zawiera profilu przeglądarki ani node_modules. Nie publikuje ani nie zastępuje aktywnej aplikacji.`);
}

async function report(argument) {
  if (!argument) throw new Error('Podaj folder aktualizacji zwrócony przez polecenie start.');
  const allowed = await realpath(updates);
  const session = await realpath(resolve(project, argument));
  const tail = relative(allowed, session);
  if (!tail || tail.startsWith(`..${sep}`) || tail === '..' || isAbsolute(tail) || tail.includes(sep)) throw new Error('Nieprawidłowy folder aktualizacji.');
  const baseline = join(session, 'przed');
  const candidate = join(session, 'propozycja');
  const original = new Map(Object.entries(JSON.parse(await readFile(join(session, 'manifest-przed.json'), 'utf8'))));
  const before = await scan(baseline);
  if (before.size !== original.size || [...original].some(([name, hash]) => before.get(name) !== hash)) throw new Error('Kopia przed aktualizacją różni się od manifestu. Nie tworzymy raportu z niewiarygodnego punktu odniesienia.');
  const after = await scan(candidate);
  const active = await scan(project);
  const changed = [...new Set([...before.keys(), ...after.keys()])].filter(name => before.get(name) !== after.get(name)).sort();
  const activeChanged = [...new Set([...before.keys(), ...active.keys()])].filter(name => before.get(name) !== active.get(name)).sort();
  const out = ['# Raport zmian aktualizacji', '', `Porównano ${before.size} plików sprzed aktualizacji z ${after.size} plikami propozycji.`, 'Raport to podgląd techniczny, nie dowód zgodności źródeł ani wynik testów. Długie wartości mogą być ucięte.', ''];
  out.push('## Zmiany w aktywnym projekcie od utworzenia kopii', '');
  if (activeChanged.length) out.push('Aktywny projekt zmienił się niezależnie. Nie zastępuj go kopią; porównaj i połącz zmiany ręcznie:', ...activeChanged.map(name => `- ${name}`));
  else out.push('Nie wykryto zmian w porównywanych plikach aktywnego projektu.');
  out.push('');
  if (!changed.length) out.push('Brak zmian w porównywanych plikach.');
  for (const name of changed) {
    const status = !before.has(name) ? 'dodano' : !after.has(name) ? 'usunięto' : 'zmieniono';
    out.push(`## ${name} — ${status}`);
    if (name === 'src/data/source-policy.json') out.push('UWAGA: zmieniono politykę źródeł. Sprawdź, czy użytkownik wyraźnie zlecił zmianę rejestru wykluczeń.');
    if (status === 'zmieniono' && name.startsWith('src/data/') && name.endsWith('.json')) {
      try { out.push(...diffJson(JSON.parse(await readFile(join(baseline, name), 'utf8')), JSON.parse(await readFile(join(candidate, name), 'utf8')))); }
      catch { out.push('Nie można porównać zawartości JSON — sprawdź składnię i plik ręcznie.'); }
    } else out.push('Sprawdź pełną zawartość zmiany ręcznie, zwłaszcza źródła, roczniki i kod.');
    out.push('');
  }
  const path = join(session, 'raport-zmian.md');
  await writeFile(path, out.join('\n') + '\n', 'utf8');
  console.log(`Zmienione pliki propozycji: ${changed.length}\nZmiany aktywnego projektu od utworzenia kopii: ${activeChanged.length}\nRaport: ${path}\nRaport nie podmienia danych i nie publikuje aplikacji.`);
}

try {
  if (process.argv[2] === 'start') await start();
  else if (process.argv[2] === 'report') await report(process.argv[3]);
  else throw new Error('Użycie: node scripts/update-workspace.mjs start | report <folder-aktualizacji>');
} catch (error) { console.error(`Błąd: ${error.message}`); process.exitCode = 1; }
