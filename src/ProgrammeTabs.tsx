import { useState } from 'react';
import type { ReactNode, KeyboardEvent } from 'react';
import type { Programme, Profile, AdmissionRule } from './types';
import AdmissionPanel from './AdmissionPanel';
import ThresholdPanel from './ThresholdPanel';
import CareerPanel from './CareerPanel';
import GraduateOutcomesPanel from './GraduateOutcomesPanel';
import CurriculumPanel from './CurriculumPanel';
import ProgrammeDescriptionPanel from './ProgrammeDescriptionPanel';
import './programme-tabs.css';

const tabs = [
  { id: 'description', label: 'Opis kierunku' },
  { id: 'programme', label: 'Program i specjalności' },
  { id: 'admission', label: 'Rekrutacja' },
  { id: 'history', label: 'Progi przyjęć' },
  { id: 'graduates', label: 'Losy absolwentów' },
  { id: 'career', label: 'Zawód i perspektywy' },
  { id: 'notes', label: 'Notatki i źródła' },
];

export default function ProgrammeTabs({ programme, profile, update, rule, sources }: {
  programme: Programme; profile: Profile; update: (profile: Profile) => void;
  rule?: AdmissionRule; sources: ReactNode;
}) {
  const [active, setActive] = useState('description');
  const prefix = `programme-${programme.id}`;
  function move(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    let next: number;
    if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    else return;
    event.preventDefault();
    setActive(tabs[next].id);
    document.getElementById(`${prefix}-tab-${tabs[next].id}`)?.focus();
  }
  const content: Record<string, ReactNode> = {
    description: <ProgrammeDescriptionPanel programme={programme}/>,
    programme: <CurriculumPanel programme={programme}/>,
    admission: <><AdmissionPanel programme={programme} profile={profile} update={update} rule={rule}/><details><summary>Pełna uwaga o zasadach rekrutacji</summary><p>{programme.admissionNote}</p><p><strong>Przedmioty maturalne:</strong> {programme.subjects.join(', ') || 'Sprawdź kartę źródłową'}</p></details></>,
    history: <ThresholdPanel programme={programme}/>,
    graduates: <GraduateOutcomesPanel programme={programme}/>,
    career: <><h3>Możliwe ścieżki zawodowe</h3><ul className="careers">{programme.careers.map(c => <li key={c}>{c}</li>)}</ul><p className="muted">{programme.careerNote}</p><CareerPanel programme={programme} profile={profile} update={update}/></>,
    notes: <><label className="field-label">Twoje notatki i wybrana ścieżka<textarea maxLength={20000} value={profile.notes[programme.id] ?? ''} onChange={event => update({ ...profile, notes: { ...profile.notes, [programme.id]: event.target.value } })} placeholder="Co chcesz sprawdzić? Która ścieżka Cię interesuje?"/></label><h3>Źródła tej oferty</h3>{sources}</>,
  };
  return <div className="programme-tabs">
    <div className="programme-tablist" role="tablist" aria-label="Sekcje kierunku">{tabs.map((tab, index) => <button className="programme-tab" type="button" role="tab" id={`${prefix}-tab-${tab.id}`} key={tab.id} aria-selected={active === tab.id} aria-controls={`${prefix}-panel-${tab.id}`} tabIndex={active === tab.id ? 0 : -1} onClick={() => setActive(tab.id)} onKeyDown={event => move(event, index)}>{tab.label}</button>)}</div>
    {tabs.map(tab => <section className="programme-tabpanel" role="tabpanel" id={`${prefix}-panel-${tab.id}`} key={tab.id} aria-labelledby={`${prefix}-tab-${tab.id}`} tabIndex={0} hidden={active !== tab.id}>{content[tab.id]}</section>)}
  </div>;
}
