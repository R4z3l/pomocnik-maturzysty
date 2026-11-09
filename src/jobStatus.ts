export type JobStatus = 'confirmed' | 'unconfirmed' | 'expired';

export function displayJobStatus(job: { active: string; expiresAt: string | null }, today: string): JobStatus {
  if (job.active === 'expired' || (job.expiresAt !== null && job.expiresAt < today)) return 'expired';
  return job.active === 'confirmed' ? 'confirmed' : 'unconfirmed';
}

export function localDate(date: Date): string {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}
