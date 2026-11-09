import {sourceExclusion} from '../src/sources.ts';
const [url,purpose='current']=process.argv.slice(2);
if(!url||!['current','history'].includes(purpose)){console.error('Użycie: node --experimental-strip-types scripts/check-source.ts URL [current|history]');process.exit(2);}
try{const excluded=sourceExclusion(url,purpose as 'current'|'history');if(excluded){console.error('POMIŃ: '+excluded.reason);process.exit(1);}console.log('OK: adres nie jest wykluczony. Nadal wymaga sprawdzenia treści i rocznika.');}
catch{console.error('Nieprawidłowy URL.');process.exit(2);}
