import policy from './data/source-policy.json' with {type:'json'};
import type {Source} from './types.ts';
export const sourcePolicy=policy;
export type SourcePurpose='current'|'history';
function canonical(value:string){
 const u=new URL(value);u.hash='';u.hostname=u.hostname.toLowerCase().replace(/^www\./,'');
 for(const key of [...u.searchParams.keys()])if(key.startsWith('utm_')||['fbclid','gclid'].includes(key))u.searchParams.delete(key);
 u.searchParams.sort();
 return {host:u.hostname,path:u.pathname.replace(/\/$/,'')||'/',query:u.searchParams.toString()};
}
export function sourceExclusion(url:string,purpose:SourcePurpose='current') {
 const candidate=canonical(url);
 return policy.excludedPages.find(entry=>{
  if(entry.scope==='current'&&purpose==='history')return false;
  const blocked=canonical(entry.url);
  if(candidate.host!==blocked.host)return false;
  if(entry.match==='host')return true;
  if(entry.match==='prefix')return candidate.path===blocked.path||candidate.path.startsWith(blocked.path+'/');
  return candidate.path===blocked.path&&candidate.query===blocked.query;
 });
}
export function sourcePriority(source:Source):number {
 if(source.kind==='community')return 5;
 if(source.kind==='official')return 1;
 if(source.kind==='press')return 4;
 return canonical(source.url).host==='otouczelnie.pl'?2:3;
}
export function compareSources(a:Source,b:Source):number {
 const rank=(s:Source)=>sourceExclusion(s.url)?99:sourcePriority(s);
 return rank(a)-rank(b)||a.title.localeCompare(b.title,'pl');
}

export function claimRejection(url:string,programmeId:string,year:string){
 const page=canonical(url);
 return policy.rejectedClaims.find(c=>{const rejected=canonical(c.url);return c.programmeId===programmeId&&c.year===year&&page.host===rejected.host&&page.path===rejected.path&&page.query===rejected.query;});
}
