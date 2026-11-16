import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, copyFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

test('izolowana aktualizacja pokazuje zmiany i wykrywa uszkodzenie punktu odniesienia', () => {
  const root = mkdtempSync(join(tmpdir(), 'studia-update-test-'));
  assert.ok(resolve(root).startsWith(resolve(tmpdir()) + requireSeparator()));
  try {
    for (const dir of ['src/data', 'scripts', 'tests', 'public', 'docs']) mkdirSync(join(root, dir), { recursive: true });
    for (const name of ['AGENTS.md', 'README.md', 'package.json', 'package-lock.json', 'tsconfig.json', 'index.html']) writeFileSync(join(root, name), '{}');
    copyFileSync(new URL('../scripts/update-workspace.mjs', import.meta.url), join(root, 'scripts/update-workspace.mjs'));
    writeFileSync(join(root, 'requirements-data.txt'), 'requests==2.32.5\n');
    writeFileSync(join(root, 'src/data/example.json'), JSON.stringify([{ id: 'a', value: 1 }]));
    const run = (...args: string[]) => spawnSync(process.execPath, [join(root, 'scripts/update-workspace.mjs'), ...args], { cwd: root, encoding: 'utf8' });
    const start = run('start');
    assert.equal(start.status, 0, start.stderr);
    const updates = join(root, 'output/aktualizacje-ai');
    const session = start.stdout.match(/Folder aktualizacji: (.+)/)?.[1]?.trim();
    assert.ok(session && basename(session).startsWith('aktualizacja-') && resolve(session).startsWith(resolve(updates) + requireSeparator()));
    assert.equal(readFileSync(join(session, 'propozycja/requirements-data.txt'), 'utf8'), 'requests==2.32.5\n');
    writeFileSync(join(session, 'propozycja/src/data/example.json'), JSON.stringify([{ id: 'a', value: 2 }]));
    writeFileSync(join(root, 'src/data/example.json'), JSON.stringify([{ id: 'a', value: 3 }]));
    const report = run('report', session);
    assert.equal(report.status, 0, report.stderr);
    const text = readFileSync(join(session, 'raport-zmian.md'), 'utf8');
    assert.match(text, /id=a\]\.value: 1 → 2/);
    assert.match(text, /Aktywny projekt zmienił się niezależnie/);
    assert.match(readFileSync(join(root, 'src/data/example.json'), 'utf8'), /"value":3/);
    writeFileSync(join(session, 'przed/src/data/example.json'), '[]');
    const tampered = run('report', session);
    assert.equal(tampered.status, 1);
    assert.match(tampered.stderr, /różni się od manifestu/);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

function requireSeparator() { return process.platform === 'win32' ? '\\' : '/'; }
