import type { AdmissionRule, Profile } from './types.ts';
import type { AdmissionResult } from './admission.ts';

// Polska nowa matura PP/PR: oba poziomy tego samego przedmiotu mogą się sumować.
export function calculatePwrAdmission(rule: AdmissionRule, profile: Profile): AdmissionResult {
  if (Object.keys(profile.bilingualScores ?? {}).length) return {
    total: null, maturaTotal: null, status: 'missing', rows: [],
    issues: ['Profil zawiera maturę dwujęzyczną. Kalkulator Politechniki Wrocławskiej obsługuje PP/PR; odrębny przelicznik i dodatkowe egzaminy w języku obcym wymagają ręcznej weryfikacji.'],
  };
  let missing = false;
  let requirement = false;
  const issues: string[] = [];
  const rows = rule.groups.map(group => {
    let best = 0;
    let subject = '';
    let detail = 'Przedmiot niezdawany — 0 pkt.';
    let pending = false;
    for (const name of group.subjects) {
      const basic = group.factors.basic ? profile.basicScores?.[name] : undefined;
      const extended = group.factors.extended ? profile.subjects[name] : undefined;
      if (basic === null || extended === null) pending = true;
      for (const value of [basic, extended]) if (typeof value === 'number' && (!Number.isFinite(value) || value < 0 || value > 100)) throw new Error('Wynik matury poza zakresem.');
      const p = basic ?? 0;
      const r = extended ?? 0;
      const combined = group.factors.basic === 1 && group.factors.extended === 2.5;
      const value = (combined ? Math.max(p, p + 1.5*r, 2.5*r) : Math.max(p*group.factors.basic, r*group.factors.extended)) * group.weight;
      if (value > best || !subject && (basic !== undefined || extended !== undefined)) {
        best = value; subject = name;
        detail = `${name}: P = ${p}%, R = ${r}%; ${combined ? 'max(P, P + 1,5R, 2,5R)' : `max(P × ${group.factors.basic}, R × ${group.factors.extended})`} × ${group.weight}.`;
      }
    }
    if (pending) missing = true;
    return { label: group.label, subject, value: pending ? null : best, detail: pending ? 'Zaznaczony poziom bez wyniku. Uzupełnij procent albo odznacz niezdawany poziom.' : detail };
  });
  const medical = rule.groups[0].label === 'Biologia rozszerzona';
  if (!missing && !medical && rows[0].value === 0 && rows[1].value === 0) {
    for (const row of rows.slice(2)) { row.value = 0; row.detail += ' Przy M = 0 i PD = 0 składniki językowe wynoszą 0.'; }
  }
  let maturaTotal = missing ? null : rows.reduce((sum, row) => sum + (row.value ?? 0), 0);
  if (!missing && medical && (rows[0].value === 0 || rows[1].value === 0)) {
    maturaTotal = 0; requirement = true;
    issues.push('Biologia rozszerzona i matematyka muszą dać wynik większy od 0. Przy B = 0 lub M = 0 cały WM wynosi 0.');
  }
  let extra = 0;
  if (rule.extraExam) {
    const exam = rule.extraExam;
    const value = profile.admissionExtras?.[rule.id];
    if (value === undefined || value === null) {
      missing = true;
      rows.push({ label: exam.label, subject: '', value: null, detail: 'Brak wyniku dodatkowego etapu — nie zastępujemy go zerem.' });
    } else {
      if (!Number.isFinite(value) || value < exam.min || value > exam.max) throw new Error('Wynik egzaminu poza skalą.');
      extra = value;
      rows.push({ label: exam.label, subject: '', value, detail: `Skala ${exam.min}–${exam.max}; zaliczenie od ${exam.passMin}.` });
      if (value < exam.passMin) { requirement = true; issues.push(`Egzamin z rysunku wymaga co najmniej ${exam.passMin} pkt.`); }
    }
  }
  const total = missing || maturaTotal === null ? null : maturaTotal + extra;
  if (total !== null && rule.minimumTotal !== undefined && total < rule.minimumTotal) {
    requirement = true; issues.push(`Minimum formalne wynosi ${rule.minimumTotal} pkt.`);
  }
  return { total, maturaTotal, rows, issues, status: requirement ? 'requirement' : missing ? 'missing' : 'complete' };
}
