export default function AppIcon({ name }: { name: string }) {
  const paths: Record<string, string> = {
    catalogue: 'M4 5h6v6H4z M14 5h6v6h-6z M4 15h6v6H4z M14 15h6v6h-6z',
    universities: 'M3 10 12 4l9 6M5 10v10m7-10v10m7-10v10M3 21h18',
    profile: 'M8 7a4 4 0 1 0 8 0 4 4 0 1 0-8 0M4 21v-2a8 8 0 0 1 16 0v2',
    compare: 'M4 8h12m-4-4 4 4-4 4M20 16H8m4-4-4 4 4 4',
    sources: 'M5 3h10l4 4v14H5zM14 3v5h5M8 12h8m-8 4h6',
    recommendations: 'm12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5z',
    instructions: 'M5 4h14v17H5zM8 8h8m-8 4h8m-8 4h5',
    heart: 'M20.5 5.5a5 5 0 0 0-7 0L12 7l-1.5-1.5a5 5 0 0 0-7 7L12 21l8.5-8.5a5 5 0 0 0 0-7z',
    study: 'm2 9 10-5 10 5-10 5zM6 11v6c4 3 8 3 12 0v-6m4-2v8',
    menu: 'M4 6h16M4 12h16M4 18h16',
  };
  return <svg className="app-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false"><path d={paths[name] || paths.study}/></svg>;
}
