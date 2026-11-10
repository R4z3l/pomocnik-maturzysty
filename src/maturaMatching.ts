import { calculateAdmission, UEW_EN, UEW_PL } from './admission.ts';
import type { AdmissionRule, Profile, Programme } from './types.ts';

export const MATCHING_HISTORY_YEAR = '2026/2027';

// Reuse the actual formula (including alternatives, exclusions and PWr's sums).
// Only PR capacity is ranked: results and PP belong to the separate calculator.
export function extensionFit(rule: AdmissionRule, selected: string[]) {
  const subjects = [...new Set(rule.groups.flatMap(g => (g.options ?? g.subjects.map(subject => ({ subject }))).map(o => o.subject)))];
  const rewarded = [...new Set(rule.groups.flatMap(g => (g.options ?? g.subjects.map(subject => ({ subject, ...g.factors })))
    .filter(o => o.extended * g.weight > 0 && selected.includes(o.subject)).map(o => o.subject)))];
  const simulate = (enabled: string[]) => calculateAdmission(rule, {
    version: 1, subjects: Object.fromEntries(subjects.map(s => [s, enabled.includes(s) ? 100 : 0])),
    interests: '', workStyle: '', favorites: [], comparison: [], notes: {}, weights: [], ratings: {},
  }).rows.filter(row => row.subject && row.value !== null);
  const capacity = simulate(subjects).reduce((sum, row) => sum + row.value!, 0);
  const rows = simulate(selected).filter(row => row.value! > 0);
  const points = rows.reduce((sum, row) => sum + row.value!, 0);
  return { ratio: capacity ? points / capacity : 0, rows, capacity, points, rewarded };
}

export function matchMatura(programmes: Programme[], rules: AdmissionRule[], profile: Profile) {
  return programmes.map(programme => {
    const rule = rules.find(r => r.id === programme.admissionRuleId);
    const fit = rule ? extensionFit(rule, Object.keys(profile.subjects)) : null;
    const score = rule ? calculateAdmission(rule, profile) : null;
    // A threshold's year is not evidence that the current formula applied then.
    // UEW has separately verified 2026 rules; other universities remain explicit gaps.
    const historicalRule = rule?.year === MATCHING_HISTORY_YEAR ? rule
      : rule?.id === 'uew-2027-pl' ? UEW_PL : rule?.id === 'uew-2027-en' ? UEW_EN : null;
    const historicalScore = historicalRule ? calculateAdmission(historicalRule, profile) : null;
    const thresholds = programme.thresholds.filter(t => t.year === MATCHING_HISTORY_YEAR).map(threshold => {
      const comparable = threshold.status === 'official' && historicalScore?.status === 'complete' && historicalScore.total !== null;
      const delta = comparable ? historicalScore!.total! - threshold.value : null;
      const reason = threshold.status !== 'official' ? 'Próg zewnętrzny bez oficjalnego potwierdzenia.'
        : !historicalRule ? 'Brak zweryfikowanego wzoru dla tego naboru.'
        : historicalScore?.status !== 'complete' ? 'Uzupełnij wyniki lub sprawdź warunki kalkulatora historycznego.' : '';
      return { threshold, delta, reason };
    });
    const reachesThreshold = score?.status === 'complete' && thresholds.some(t => t.delta !== null && t.delta >= -1e-9);
    return { programme, rule, fit, score, historicalRule, historicalScore, thresholds, reachesThreshold };
  }).sort((a, b) => (b.fit?.ratio ?? -1) - (a.fit?.ratio ?? -1)
    || a.programme.name.localeCompare(b.programme.name, 'pl') || a.programme.id.localeCompare(b.programme.id));
}
