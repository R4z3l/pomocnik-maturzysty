import uwr from './data/uwr.json';
import uew from './data/uew.json';
import pwr from './data/pwr.json';
import upwr from './data/upwr.json';
import upwrRules from './data/upwr-rules.json';
import umw from './data/umw.json';
import umwRules from './data/umw-rules.json';
import pwrRules from './data/pwr-rules.json';
import uwrRules from './data/uwr-rules.json';
import {compareSources} from './sources';
import { UEW_PL, UEW_EN, UEW_PL_2027, UEW_EN_2027 } from './admission';
import type { Catalogue, AdmissionRule } from './types';

export const admissionRules: AdmissionRule[] = [UEW_PL, UEW_EN, UEW_PL_2027, UEW_EN_2027, ...uwrRules as AdmissionRule[], ...pwrRules as AdmissionRule[], ...upwrRules as AdmissionRule[], ...umwRules as AdmissionRule[]];
export const catalogue: Catalogue = {
  version: '2026-11-10-piec-uczelni',
  checkedAt: '2026-11-10',
  scopeNote: 'Stacjonarne studia I stopnia i jednolite magisterskie we Wrocławiu, po polsku i angielsku. Oferta, programy studiów, zasady rekrutacji i progi historyczne mają odrębne roczniki. Opublikowane zasady 2027/28 nie potwierdzają uruchomienia każdego kierunku. Zakres i daty sprawdzenia podajemy na fiszkach uczelni oraz kartach kierunków.',
  universities: [...uwr.universities, ...uew.universities, ...pwr.universities, ...upwr.universities, ...umw.universities],
  sources: ([...uwr.sources, ...uew.sources, ...pwr.sources, ...upwr.sources, ...umw.sources] as Catalogue['sources']).sort(compareSources),
  programmes: [...uwr.programmes, ...uew.programmes.map(p => ({...p, admissionRuleId: p.language === 'en' ? UEW_EN_2027.id : UEW_PL_2027.id})), ...pwr.programmes, ...upwr.programmes, ...umw.programmes].map(p => ({...p, subjects: [...new Set(p.subjects)]})) as Catalogue['programmes'],
};
