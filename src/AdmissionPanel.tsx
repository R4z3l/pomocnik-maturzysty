import { useState } from 'react';
import type { AdmissionRule, Profile, Programme } from './types';
import { calculateAdmission } from './admission';
import type { AdmissionResult } from './admission';
import { admissionRules } from './catalogue';

type Props={programme:Programme;rule:AdmissionRule|undefined;profile:Profile;update:(p:Profile)=>void};
export default function AdmissionPanel({programme,rule,profile,update}:Props) {
 const [chosen,setChosen]=useState<string|null>(null);
 const alternatives=programme.universityId==='uew'?admissionRules.filter(r=>r.id.startsWith('uew-')&&r.id.endsWith('-'+programme.language)):(rule?[rule]:[]);
 const active=alternatives.find(r=>r.id===chosen)??rule;
 if(!active)return <section className="admission-documentary"><h3>Warunki dokumentowe i językowe</h3><p>{programme.admissionNote}</p><p className="muted">W sprawdzonym opisie nie opublikowano wzoru punktowego dla tej procedury. Spełnienie warunku językowego i złożenie dokumentów nie gwarantują przyjęcia. Zweryfikuj status naboru, terminy i dokumenty na oficjalnej karcie.</p></section>;
 let result:AdmissionResult;
 try { result=calculateAdmission(active,profile); }
 catch { result={total:null,maturaTotal:null,status:'missing',rows:[],issues:['Wynik dodatkowego etapu w profilu jest poza dozwoloną skalą. Popraw lub wyczyść pole tego etapu poniżej.']}; }
 const format=(v:number)=>v.toLocaleString('pl',{maximumFractionDigits:3});
 const exam=active.extraExam;
 const setExtra=(value:number|null)=>update({...profile,admissionExtras:{...profile.admissionExtras,[active.id]:value}});
 return <section className="admission-result"><h3>Kalkulator · {active.year}</h3>
 {alternatives.length>1&&<label className="field-label">Rocznik zasad rekrutacji<select value={active.id} onChange={e=>setChosen(e.target.value)}>{alternatives.map(r=><option value={r.id} key={r.id}>{r.year}</option>)}</select></label>}
 <p className="muted">Rocznik zasad dotyczy obliczenia. Oferta kierunku ma rok odniesienia {programme.referenceYear}.</p>
 <details><summary>Wzór i współczynniki</summary><p>{active.formula}</p></details><p className="muted">P = poziom podstawowy; R = rozszerzony; D = dwujęzyczny. Zmień wyniki matur w „Mój profil”.</p>
 {exam&&<div className="exam-input"><h4>{exam.label}</h4><p>{exam.note}</p><label className="field-label">Wynik dodatkowego etapu {exam.allowedValues?<select value={profile.admissionExtras?.[active.id]??''} onChange={e=>setExtra(e.target.value===''?null:Number(e.target.value))}><option value="">Brak wyniku</option>{exam.allowedValues.map(v=><option key={v} value={v}>{v} pkt</option>)}</select>:<input type="number" min={exam.min} max={exam.max} step="any" value={profile.admissionExtras?.[active.id]??''} placeholder="Brak wyniku" onChange={e=>{const v=e.target.value===''?null:Number(e.target.value);if(v===null||Number.isFinite(v)&&v>=exam.min&&v<=exam.max)setExtra(v);}}/>}</label><p className="muted">Skala {exam.min}–{exam.max}; zaliczenie od {exam.passMin}. Wpis służy symulacji lub zapisaniu uzyskanego wyniku. Nie potwierdza zaproszenia do kolejnego etapu.</p></div>}
 <dl className="facts">{result.rows.map((r,i)=><div key={i}><dt>{r.label}<small>{r.detail}</small></dt><dd>{r.value===null?'brak':format(r.value)}</dd></div>)}</dl>
 {exam&&result.maturaTotal!==null&&<p><strong>Etap matur: {format(result.maturaTotal)} pkt</strong>{active.minimumMaturaTotal!==undefined&&` · minimum formalne tego etapu: ${active.minimumMaturaTotal} pkt`}</p>}
 <strong>{result.total===null?'Uzupełnij wyniki lub sprawdź warunki':`${format(result.total)} pkt${exam?' · suma etapów':''}`}</strong>
 {result.status==='requirement'&&<p role="status">Wpisane wyniki nie spełniają wszystkich opisanych warunków formalnych.</p>}
 {result.issues.length>0&&<ul className="admission-issues">{result.issues.map(t=><li key={t}>{t}</li>)}</ul>}
 <p className="muted">{active.caveat}</p><a href={active.sourceUrl} target="_blank" rel="noreferrer">Oficjalna podstawa punktacji · sprawdzono {active.checkedAt}</a><p className="muted">Minimum formalne nie jest historycznym wynikiem ostatniej przyjętej osoby. Progi historyczne mają własne roczniki i skale; nie porównujemy ich automatycznie z bieżącym wynikiem. Wynik nie gwarantuje przyjęcia.</p></section>;
}
