import type { AdmissionRule, Profile } from './types.ts';
import { calculatePwrAdmission } from './pwrAdmission.ts';
const foreign=['język angielski','język niemiecki','język francuski','język hiszpański','język rosyjski','język włoski'];
const factors={basic:0.5,extended:1,bilingual:0};
export const UEW_PL: AdmissionRule = {id:'uew-2026-pl',year:'2026/2027',title:'Uniwersytet Ekonomiczny we Wrocławiu — polska matura od2005, tryb zwykły',formula:'M + J + X; wybór najwyższego wyniku po przeliczeniu w każdej grupie',sourceUrl:'https://rekrutacja.uew.pl/en/studia-i-stopnia-zasady-rekrutacji/',checkedAt:'2026-10-24',groups:[
  {label:'Matematyka',subjects:['matematyka'],factors,weight:1},
  {label:'Język obcy',subjects:foreign,factors:{...factors,bilingual:1.5},weight:1},
  {label:'Przedmiot do wyboru',subjects:['język polski','geografia','historia','WOS','fizyka','chemia','biologia','informatyka','filozofia'],factors,weight:1}
],caveat:'Zasady 2026/27, nie potwierdzenie naboru2027/28. Nie obejmuje starej matury, IB/EB, olimpiad ani punktów dodatkowych przyznawanych na wniosek. Gdy nie zdawano przedmiotu, uczelnia przewiduje wariant oceny szkolnej dla PL — tutaj pozostaje do ręcznego przeliczenia. Wynik to punkty, nie gwarancja przyjęcia.'};
export const UEW_EN: AdmissionRule={...UEW_PL,id:'uew-2026-en',title:'Uniwersytet Ekonomiczny we Wrocławiu — studia anglojęzyczne',groups:UEW_PL.groups.map(g=>g.label==='Język obcy'?{...g,subjects:['język angielski'],factors:{basic:0,extended:1,bilingual:1.5},minPercent:60}:g),caveat:'Angielski rozszerzony lub dwujęzyczny minimum60%; podstawowy nie spełnia tego warunku. Wariant ocen szkolnych nie dotyczy żadnego przedmiotu przy EN. Pozostałe ograniczenia: zwykła polska matura, reguła2026/27, bez punktów dodatkowych i gwarancji przyjęcia.'};
export const UEW_PL_2027: AdmissionRule = {
  ...UEW_PL,id:'uew-2027-pl',year:'2027/2028',checkedAt:'2026-10-25',
  title:'Uniwersytet Ekonomiczny we Wrocławiu — polska matura, rekrutacja 2027/2028',
  sourceUrl:'https://www.bip.ue.wroc.pl/download/attachment/4202/uchwala-senatu-r0000262026.pdf?v=1782885195',
  groups:UEW_PL.groups.map(g=>g.label==='Przedmiot do wyboru'?{...g,subjects:[...g.subjects,'biznes i zarządzanie']}:g),
  caveat:'Uchwała R.0000.26.2026 z 25.06.2026, §4, s.5–9: zasady 2027/28 dla obywateli polskich z nową maturą pisemną. Podstawa ×0,5; rozszerzenie ×1; język dwujęzyczny ×1,5. Dodano biznes i zarządzanie. Nie obejmuje starej matury, IB/EB, ocen szkolnych, olimpiad ani indywidualnych rozstrzygnięć; dodatkowe uprawnienia wymagają osobnej weryfikacji. Przy remisie możliwe dodatkowe kryterium komisji. Oferta kierunku jest potwierdzona dla 2026/27; opublikowane zasady nie potwierdzają uruchomienia każdego kierunku w 2027/28.'
};
export const UEW_EN_2027: AdmissionRule = {...UEW_PL_2027,id:'uew-2027-en',title:'Uniwersytet Ekonomiczny we Wrocławiu — kierunki anglojęzyczne, rekrutacja 2027/2028',groups:UEW_PL_2027.groups.map(g=>g.label==='Język obcy'?{...g,subjects:['język angielski'],factors:{basic:0,extended:1,bilingual:1.5},minPercent:60}:g),caveat:UEW_PL_2027.caveat+' Angielski wyłącznie rozszerzony albo dwujęzyczny, minimum 60%. Wariant ocen szkolnych nie dotyczy żadnego przedmiotu na kierunkach anglojęzycznych.'};
export interface AdmissionResult {total:number|null;maturaTotal:number|null;status:'missing'|'requirement'|'complete';rows:{subject:string;label:string;value:number|null;detail:string}[];issues:string[]}
export function calculateAdmission(rule: AdmissionRule, p: Profile): AdmissionResult {
  if (rule.id.startsWith('pwr-')) return calculatePwrAdmission(rule, p);
  if((rule.id.startsWith('uwr-') || rule.id.startsWith('upwr-') || rule.id.startsWith('umw-') && !rule.groups.some(g=>g.factors.bilingual>0)) && Object.keys(p.bilingualScores??{}).length) {
    return {total:null,maturaTotal:null,issues:[],status:'missing' as const,rows:[{subject:'',label:'Matura dwujęzyczna — wymaga odrębnego sprawdzenia',value:null,detail:'Profil zawiera poziom dwujęzyczny. Ten wariant kalkulatora obsługuje tylko PP/PR; sprawdź odrębny przelicznik na oficjalnej karcie. Nie pomijamy tego wyniku w sumie.'}]};
  }
  const scores={basic:p.basicScores??{},extended:p.subjects,bilingual:p.bilingualScores??{}};
  const names={basic:'podst.',extended:'rozsz.',bilingual:'dwujęz.'};
  type Candidate={subject:string;value:number|null;detail:string;label:string};
  let missing=false, requirement=false;
  const groups=rule.groups.map(g=>{
    let pending=false, below=false;
    const candidates:Candidate[]=[];
    const options=g.options??g.subjects.map(subject=>({subject,...g.factors}));
    for(const option of options) for(const level of ['basic','extended','bilingual'] as const) {
      const factor=option[level]; if(!factor)continue;
      const value=scores[level][option.subject]; if(value===undefined)continue;
      if(value===null){pending=true;continue;}
      if(!Number.isFinite(value)||value<0||value>100)throw new Error('Wynik matury poza zakresem.');
      if(g.minPercent!==undefined && value<g.minPercent){below=true;continue;}
      const points=value*factor*g.weight;
      const finalPoints=g.rounding==='integer'?Math.round(points):points;
      if(g.minPoints!==undefined && finalPoints<g.minPoints){below=true;continue;}
      candidates.push({subject:option.subject,label:g.label,value:finalPoints,detail:option.subject+' '+names[level]+': '+value+'% × '+factor+' × '+g.weight+(g.rounding==='integer'?' (zaokrąglenie do liczby całkowitej)':'')});
    }
    if(pending){missing=true;return [{subject:'',label:g.label,value:null,detail:'Zaznaczony przedmiot bez wyniku. Uzupełnij procent albo odznacz niezdawany poziom.'}];}
    if(g.optional)candidates.push({subject:'',label:g.label,value:0,detail:'Brak przedmiotu; reguła dopuszcza 0 punktów.'});
    if(!candidates.length){if(below)requirement=true;else missing=true;return [{subject:'',label:g.label,value:null,detail:below?'Wynik poniżej minimum '+(g.minPoints!==undefined?g.minPoints+' pkt.':g.minPercent+'%.'):'Brak wyniku dla tej grupy.'}];}
    return candidates;
  });
  let best:Candidate[]|null=null, bestTotal=-Infinity;
  function visit(index:number, selected:Candidate[], total:number) {
    if(index===groups.length){if(total>bestTotal){bestTotal=total;best=[...selected];}return;}
    for(const c of groups[index]) {
      if(c.subject && rule.groups[index].excludeSubjectsFromGroups?.some(i=>selected[i]?.subject===c.subject))continue;
      selected.push(c);visit(index+1,selected,total+(c.value??0));selected.pop();
    }
  }
  visit(0,[],0);
  if(best===null){missing=true;}
  const rows:Candidate[]=best??groups.map(g=>g[0]);
  const maturaTotal=missing||rows.some(r=>r.value===null)?null:bestTotal;
  const issues:string[]=[];
  if(maturaTotal!==null && rule.minimumMaturaTotal!==undefined && maturaTotal<rule.minimumMaturaTotal) {
    requirement=true;issues.push(`Etap matur wymaga co najmniej ${rule.minimumMaturaTotal} pkt. Punkty rozmowy nie zastępują tego warunku.`);
  }
  for(const condition of rule.requirements??[]) {
    const passed=condition.options.some(o=>{const value=scores[o.level][o.subject];return typeof value==='number'&&value>=o.minPercent;});
    if(passed)continue;
    const pending=condition.options.some(o=>scores[o.level][o.subject]===null);
    const known=condition.options.some(o=>typeof scores[o.level][o.subject]==='number');
    if(pending||!known)missing=true;else requirement=true;
    issues.push(`${condition.label}: wymagane ${condition.options.map(o=>`${o.subject} ${names[o.level]} co najmniej ${o.minPercent}%`).join(' lub ')}. ${pending||!known?'Uzupełnij wyniki.':'Wpisane wyniki nie spełniają warunku.'}`);
  }
  let extra=0;
  if(rule.extraExam) {
    const exam=rule.extraExam,value=p.admissionExtras?.[rule.id];
    if(value===undefined||value===null) {
      missing=true;rows.push({subject:'',label:exam.label,value:null,detail:'Brak wyniku dodatkowego etapu; nie zastępujemy go zerem.'});
    } else {
      if(!Number.isFinite(value)||value<exam.min||value>exam.max||exam.allowedValues&&!exam.allowedValues.includes(value))throw new Error('Wynik dodatkowego etapu poza dozwoloną skalą.');
      extra=value;rows.push({subject:'',label:exam.label,value,detail:`Wynik dodatkowego etapu; minimum zaliczenia ${exam.passMin} pkt.`});
      if(value<exam.passMin){requirement=true;issues.push(`${exam.label}: wymagane co najmniej ${exam.passMin} pkt.`);}
    }
  }
  const total=missing||maturaTotal===null?null:maturaTotal+extra;
  if(total!==null && rule.minimumTotal!==undefined && total<rule.minimumTotal){requirement=true;issues.push(`Wymagane minimum formalne: ${rule.minimumTotal} pkt.`);}
  return {total,maturaTotal,status:requirement?'requirement':missing?'missing':'complete',rows,issues};
}
