import type { Threshold, Source } from './types.ts';
import {sourcePriority,sourceExclusion,sourcePolicy} from './sources.ts';
export const HISTORY_YEARS=sourcePolicy.history.admissionYears.map(year=>`${year}/${year+1}`);
export function historyCoverage(thresholds:Threshold[],sources:Source[]=[]) {
 return HISTORY_YEARS.map(year=>{
   const rank=(t:Threshold)=>{const s=sources.find(s=>s.id===t.sourceId);return s?sourcePriority(s):t.status==='official'?1:t.status==='anecdote'?5:3;};
   const rows=thresholds.filter(t=>{const source=sources.find(s=>s.id===t.sourceId);return t.year===year&&(!source||!sourceExclusion(source.url,'history'));}).sort((a,b)=>rank(a)-rank(b));
   const discrepancy=rows.some((a,i)=>rows.slice(i+1).some(b=>a.sourceId!==b.sourceId&&a.value!==b.value&&(!a.basis||a.basis==='unspecified'||!b.basis||b.basis==='unspecified'||a.basis===b.basis)));
   return {year,rows,discrepancy};
 });
}
