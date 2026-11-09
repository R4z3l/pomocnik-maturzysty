import {test} from 'node:test';
import assert from 'node:assert/strict';
import {sourcePriority,sourceExclusion,compareSources,claimRejection} from '../src/sources.ts';
import type {Source} from '../src/types.ts';
const source=(id:string,url:string,kind:Source['kind']):Source=>({id,url,kind,title:id,publisher:id,checkedAt:'2026-10-25',note:''});
test('hierarchia: uczelnia, otouczelnie, inne portale, prasa, społeczność',()=>{
 const official=source('uni','https://rekrutacja.uwr.edu.pl','official');
 const oto=source('oto','https://www.otouczelnie.pl/x','portal');
 const other=source('portal','https://www.uczelnie.pl/x','portal');
 assert.equal(sourcePriority(official),1);assert.equal(sourcePriority(oto),2);assert.equal(sourcePriority(other),3);
 assert.equal(sourcePriority(source('fake','https://otouczelnie.pl.example.org/x','portal')),3);
 assert.equal(sourcePriority(source('comment','https://www.otouczelnie.pl/x','community')),5);
 assert.deepEqual([other,oto,official].sort(compareSources).map(s=>s.id),['uni','oto','portal']);
});
test('wykluczenie respektuje cel, host, parametry roku i nie obejmuje całego poprawnego portalu',()=>{
 assert.ok(sourceExclusion('https://wroclaw.mapaakademicka.pl/mapa/x','history'));
 assert.ok(sourceExclusion('https://study.uni.wroc.pl/vademecum/','current'));
 assert.equal(sourceExclusion('https://study.uni.wroc.pl/vademecum/','history'),undefined);
 assert.ok(sourceExclusion('https://www.opinieouczelniach.pl/uczelnia/uniwersytet-ekonomiczny-we-wroclawiu/kalendarz-akademicki/?utm_source=test'));
 assert.equal(sourceExclusion('https://opinieouczelniach.pl/uczelnia/uniwersytet-ekonomiczny-we-wroclawiu/rekrutacja/'),undefined);
 assert.equal(sourceExclusion('https://rekrutacja.uwr.edu.pl/kierunek/3?rok=6'),undefined);
});

test('odrzucony wiersz nie blokuje innego kierunku z tej samej strony',()=>{
 assert.ok(claimRejection('https://www.uczelnie.pl/progi-punktowe/ekonomia','uew-ekonomia','2025/2026'));
 assert.equal(claimRejection('https://www.uczelnie.pl/progi-punktowe/ekonomia','uwr-ekonomia','2025/2026'),undefined);
 assert.equal(claimRejection('https://www.uczelnie.pl/progi-punktowe/ekonomia','uew-ekonomia','2026/2027'),undefined);
});
