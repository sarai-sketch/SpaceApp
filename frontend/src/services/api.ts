import type {Scenario,SimResult} from '../types';
const API=import.meta.env.VITE_API_URL||'http://localhost:8000';
export async function simulate(s:Scenario):Promise<SimResult>{const r=await fetch(`${API}/api/simulaciones/ejecutar`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(s)});if(!r.ok)throw Error('No se pudo simular');return r.json()}
export async function power(lat:number,lon:number,start:string,end:string){const q=new URLSearchParams({lat:String(lat),lon:String(lon),start,end});const r=await fetch(`${API}/api/microclima/power?${q}`);if(!r.ok)throw Error('NASA POWER no disponible');return r.json()}
export async function ask(question:string,scenario:Scenario){const r=await fetch(`${API}/api/agente/chat`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question,scenario})});if(!r.ok)throw Error('Agente desconectado');return r.json()}
