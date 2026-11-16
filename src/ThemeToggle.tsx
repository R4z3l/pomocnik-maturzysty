import {useEffect,useState} from 'react';
const THEME_KEY='akcja-studia-theme';
type Theme='light'|'dark';
function initialTheme():Theme{
 try{const stored=localStorage.getItem(THEME_KEY);if(stored==='light'||stored==='dark')return stored;}catch{}
 return window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
}
export default function ThemeToggle(){
 const [theme,setTheme]=useState<Theme>(initialTheme);
 useEffect(()=>{document.documentElement.dataset.theme=theme;document.documentElement.style.colorScheme=theme;document.querySelector('meta[name="theme-color"]')?.setAttribute('content',theme==='dark'?'#131b16':'#f5f3ed');},[theme]);
 function toggle(){const next=theme==='dark'?'light':'dark';setTheme(next);try{localStorage.setItem(THEME_KEY,next);}catch{}}
 return <button className="theme-toggle" type="button" aria-label="Ciemny motyw" aria-pressed={theme==='dark'} onClick={toggle}><span aria-hidden="true">{theme==='dark'?'☀':'☾'}</span><span>{theme==='dark'?'Jasny motyw':'Ciemny motyw'}</span></button>;
}
