export interface RawCell { text: string; rowSpan: number; colSpan: number }
export interface RawTable { year: string; rows: RawCell[][] }
export interface HistoricalRow { year: string; faculty: string; programme: string; round: string; value: number | null; status: 'value' | 'missing' | 'not-opened'; raw: string; inScope: boolean }
export function parseThresholds(tables: RawTable[]): HistoricalRow[] {
  const result: HistoricalRow[] = [];
  for (const table of tables) {
    let faculty = '', remaining = 0;
    for (const cells of table.rows.slice(1)) {
      if (cells.some(c => c.colSpan !== 1)) throw new Error(`Nieobsługiwane kolumny: ${table.year}`);
      const row = [...cells];
      if (remaining === 0) {
        const heading = row.shift();
        if (!heading) throw new Error('Brak wydziału');
        faculty = heading.text.replace(/\s+/g, ' '); remaining = heading.rowSpan;
      }
      remaining--;
      if (row.length !== 4) throw new Error(`Nieprawidłowy wiersz: ${table.year}, ${faculty}`);
      const programme = row[0].text.replace(/\s+/g, ' ');
      row.slice(1).forEach((cell, i) => {
        const raw = cell.text.replace(/\s+/g, ' ').trim();
        let value: number | null = null;
        let status: HistoricalRow['status'] = 'missing';
        if (/^kierunek nieuruchomiony$/i.test(raw)) status = 'not-opened';
        else if (raw && !/^[–—-]$/.test(raw)) {
          const match = /^(\d+(?:,\d+)?)(?:\s*(?:\(\*?\d+(?: pkt)?\)|\(\*?warunek\)|\*\(\d+\)))?$/.exec(raw);
          if (!match) throw new Error(`Nieznany próg: ${raw} (${table.year}, ${programme})`);
          value = Number(match[1].replace(',', '.')); status = 'value';
        }
        result.push({ year: table.year, faculty, programme, round: ['I tura','II tura','III tura'][i], value, status, raw, inScope: !/Filia/i.test(faculty) });
      });
    }
    if (remaining !== 0) throw new Error('Niedomknięty rowspan');
  }
  return result;
}
