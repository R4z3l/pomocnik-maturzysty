import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = new URL('../dist/', import.meta.url);
const issues = [];
async function list(directory, prefix = '') {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const name = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isSymbolicLink()) issues.push(`Link symboliczny: ${name}`);
    else if (entry.isDirectory()) files.push(...await list(join(directory, entry.name), name));
    else if (entry.isFile()) files.push(name);
    else issues.push(`Nieobsługiwany element: ${name}`);
  }
  return files;
}
try {
  const files = await list(fileURLToPath(root));
  for (const file of files) {
    if (!/^(?:index\.html|favicon\.svg|assets\/index-[A-Za-z0-9_-]+\.(?:js|css))$/.test(file)) issues.push(`Nieoczekiwany plik: ${file}`);
  }
  if (!files.includes('index.html')) issues.push('Brak index.html');
  const html = await readFile(new URL('index.html', root), 'utf8');
  const referenced = [...html.matchAll(/(?:src|href)="(\/assets\/[^"?#]+)"/g)].map(match => match[1].slice(1));
  if (!referenced.some(file => file.endsWith('.js')) || !referenced.some(file => file.endsWith('.css'))) issues.push('Brak odwołania do plików aplikacji');
  for (const file of referenced) if (!files.includes(file)) issues.push(`Brak pliku wskazanego w index.html: ${file}`);
  if (issues.length) { for (const issue of issues) console.error(issue); process.exitCode = 1; }
  else console.log(`OK: ${files.length} plików w dist; tylko oczekiwane pliki aplikacji. Nie zastępuje to kontroli treści ani ochrony hostingu.`);
} catch (error) {
  console.error('Nie można sprawdzić dist. Najpierw wykonaj npm run build.', error.message);
  process.exitCode = 1;
}
