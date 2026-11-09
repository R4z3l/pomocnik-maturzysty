import type { Profile, Programme } from './types.ts';
import { SUBJECTS, CRITERIA } from './types.ts';
export function serializeProfile(profile: Profile): string {
  const text = JSON.stringify(profile);
  parseProfile(text);
  return text;
}

export function emptyProfile(): Profile {
  return { version: 1, subjects: {}, interests: '', workStyle: '', favorites: [], comparison: [], notes: {}, weights: CRITERIA.map(() => 1), ratings: {} };
}

function record(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}
function range(value: unknown, min: number, max: number): value is number {
  return typeof value === 'number' && Number.isFinite(value) && value >= min && value <= max;
}
function strings(value: unknown, max: number): value is string[] {
  return Array.isArray(value) && value.length <= max && value.every(v => typeof v === 'string' && v.length > 0 && v.length < 200) && new Set(value).size === value.length;
}

export function parseProfile(text: string): Profile {
  if (text.length > 2_000_000) throw new Error('Plik profilu jest zbyt duży (limit 2 MB).');
  const p: unknown = JSON.parse(text);
  const fail = () => { throw new Error('Nieprawidłowy profil lub nieobsługiwana wersja. Dotychczasowy profil pozostaje bez zmian.'); };
  if (!record(p) || p.version !== 1 || !record(p.subjects) || !record(p.notes) || !record(p.ratings)) return fail();
  if (typeof p.interests !== 'string' || p.interests.length > 10000 || typeof p.workStyle !== 'string' || p.workStyle.length > 10000) return fail();
  if (!strings(p.favorites, 5000) || !strings(p.comparison, 4)) return fail();
  if (!Array.isArray(p.weights) || p.weights.length !== CRITERIA.length || !p.weights.every(n => range(n, 0, 5) && Number.isInteger(n))) return fail();
  if (!Object.entries(p.subjects).every(([k,v]) => SUBJECTS.includes(k as typeof SUBJECTS[number]) && (v === null || range(v, 0, 100)))) return fail();
  const safeKey = (k: string) => k.length > 0 && k.length < 200 && !['__proto__', 'constructor', 'prototype'].includes(k);
  if (!Object.entries(p.notes).every(([k,v]) => safeKey(k) && typeof v === 'string' && v.length <= 20000)) return fail();
  if (!Object.entries(p.ratings).every(([k,v]) => safeKey(k) && Array.isArray(v) && v.length === CRITERIA.length && v.every(n => n === null || (range(n, 1, 5) && Number.isInteger(n))))) return fail();
  const extras: Partial<Profile> = {};
  for (const key of ['basicScores','bilingualScores'] as const) {
    const scores=p[key];
    if (scores === undefined) continue;
    if (!record(scores) || !Object.entries(scores).every(([s,v]) => SUBJECTS.includes(s as typeof SUBJECTS[number]) && (v===null || range(v,0,100)) && (key!=='bilingualScores' || s.startsWith('język ') && s!=='język polski' && s!=='język łaciński i kultura antyczna' && s!=='język grecki i kultura antyczna'))) return fail();
    extras[key]=scores as Record<string,number|null>;
  }
  if (p.admissionExtras !== undefined) {
    if (!record(p.admissionExtras) || !Object.entries(p.admissionExtras).every(([k,v])=>safeKey(k)&&(v===null||range(v,0,10000)))) return fail();
    extras.admissionExtras=p.admissionExtras as Record<string,number|null>;
  }
  if (p.careerChoices !== undefined) {
    if (!record(p.careerChoices) || !Object.entries(p.careerChoices).every(([k,v])=>safeKey(k)&&typeof v==='string'&&safeKey(v))) return fail();
    extras.careerChoices=p.careerChoices as Record<string,string>;
  }
  if (p.preferences !== undefined) {
    const pref=p.preferences;
    if(!record(pref)||!strings(pref.tasks,3)||!pref.tasks.every(t=>['ludzie','dane','rzeczy'].includes(t))||!['local','poland','any'].includes(String(pref.mobility))||!(pref.maxStudyYears===null||range(pref.maxStudyYears,1,15))||typeof pref.avoidShifts!=='boolean'||typeof pref.strictMobility!=='boolean')return fail();
    extras.preferences=pref as unknown as Profile['preferences'];
  }
  return { version: 1, subjects: p.subjects as Profile['subjects'], interests: p.interests, workStyle: p.workStyle, favorites: p.favorites, comparison: p.comparison, notes: p.notes as Profile['notes'], weights: p.weights, ratings: p.ratings as Profile['ratings'], ...extras };
}

export function matrixScore(weights: number[], ratings: (number | null)[]) {
  if (weights.length !== ratings.length || !weights.every(w => range(w,0,5)) || !ratings.every(r => r === null || range(r,1,5))) throw new Error('Nieprawidłowa macierz ocen.');
  const total = weights.reduce((a,b) => a+b, 0);
  if (!total) return { min: 0, max: 0, coverage: 0, disabled: true };
  let known = 0, weighted = 0, missing = 0;
  weights.forEach((weight, i) => {
    if (ratings[i] === null) missing += weight;
    else { known += weight; weighted += weight * ratings[i]!; }
  });
  return { min: (weighted + missing) / total, max: (weighted + missing * 5) / total, coverage: known / total, disabled: false };
}

export function matchSubjects(programme: Programme, profile: Profile): string {
  if (!programme.subjectsVerified || !programme.subjects.length) return 'Brak zweryfikowanej listy przedmiotów.';
  const selected = Object.keys(profile.subjects);
  if (!selected.length) return 'Wybierz rozszerzenia w profilu.';
  const common = programme.subjects.filter(s => selected.includes(s));
  return `${common.length} z ${programme.subjects.length} punktowanych przedmiotów w Twoim profilu. To nie jest ocena spełnienia warunków przyjęcia.`;
}

export function filterProgrammes(programmes: Programme[], query: string, universityId: string, language: string): Programme[] {
  const normalize = (s: string) => s.toLocaleLowerCase('pl').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ł/g, 'l');
  const words = normalize(query.trim()).split(/\s+/).filter(Boolean);
  return programmes.filter(p => (!universityId || p.universityId === universityId) && (!language || p.language === language) && words.every(word => normalize(`${p.name} ${p.fields.join(' ')}`).includes(word)));
}
