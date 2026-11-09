// Przykładowe zapytania, a nie automatyczna klasyfikacja ofert.
const terms: Record<string, { internships: string; firstJob: string }> = {
  tech: { internships: 'staż programowanie', firstJob: 'młodszy analityk danych' },
  finance: { internships: 'staż finanse', firstJob: 'młodszy księgowy' },
  business: { internships: 'staż marketing', firstJob: 'młodszy specjalista marketing' },
  law: { internships: 'staż prawo', firstJob: 'asystent prawny' },
  psychology: { internships: 'praktyki psychologia', firstJob: 'psycholog' },
  education: { internships: 'praktyki pedagogika', firstJob: 'asystent nauczyciela' },
  science: { internships: 'staż laboratorium', firstJob: 'młodszy analityk laboratoryjny' },
  humanities: { internships: 'staż komunikacja', firstJob: 'młodszy specjalista komunikacja' },
};

export function jobSearchLinks(familyId: string) {
  const selected = terms[familyId];
  if (!selected) return [];
  return Object.entries(selected).map(([level, query]) => ({
    label: level === 'internships' ? 'Praktyki i staże' : 'Pierwsza praca',
    query,
    portals: [
      { name: 'Pracuj.pl', url: `https://www.pracuj.pl/praca/${encodeURIComponent(query)}%3Bkw/wroclaw%3Bwp` },
      { name: 'Indeed', url: `https://pl.indeed.com/jobs?q=${encodeURIComponent(query)}&l=${encodeURIComponent('Wrocław, dolnośląskie')}` },
    ],
  }));
}
