import { test } from 'node:test';
import assert from 'node:assert/strict';
import { historyCoverage } from '../src/history.ts';
import type { Threshold, Source } from '../src/types.ts';
const row=(value:number,sourceId:string,basis:Threshold['basis']='unspecified'):Threshold=>({year:'2024/2025',round:null,value,status:'reported',sourceId,note:'',basis});
test('historia pokazuje braki bez zer i nie myli kwalifikacji z przyjęciem',()=>{
 const result=historyCoverage([row(135.2,'official','qualification'),row(151.75,'official','admission')]);
 assert.equal(result.length,3);
 assert.equal(result.find(r=>r.year==='2022/2023'),undefined);
 assert.equal(historyCoverage([{...row(99,'old'),year:'2023/2024'}]).flatMap(y=>y.rows).length,0);
 assert.equal(result.find(r=>r.year==='2024/2025')?.discrepancy,false);
 const disputed=historyCoverage([row(190,'portal-a'),row(203,'portal-b')]);
 assert.equal(disputed.find(r=>r.year==='2024/2025')?.discrepancy,true);
});

test('kolejność źródeł historii respektuje pierwszeństwo otouczelnie nad innymi portalami',()=>{
 const source=(id:string,url:string,kind:Source['kind']):Source=>({id,url,kind,title:id,publisher:id,checkedAt:'2026-10-25',note:''});
 const sources=[source('other','https://www.uczelnie.pl/x','portal'),source('oto','https://www.otouczelnie.pl/x','portal'),source('uni','https://rekrutacja.uew.pl/x','official')];
 const rows=[row(100,'other'),row(100,'oto'),{...row(100,'uni'),status:'official' as const}];
 assert.deepEqual(historyCoverage(rows,sources).find(y=>y.year==='2024/2025')?.rows.map(r=>r.sourceId),['uni','oto','other']);
});
