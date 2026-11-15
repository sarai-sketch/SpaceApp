from datetime import date,timedelta
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from app.services.nasa_power import get_power
router=APIRouter(prefix='/sectores',tags=['sectores y rotación'])
CROPS={'maiz','papa','haba','quinua','descanso'}
SECTORS={
'p1':dict(id='p1',name='Parcela Amanecer',community='Zona rural de ejemplo A (no verificada)',lat=-17.570,lon=-66.250,area_ha=1.4,price_bob_month=850,soil='Franco',description='Terreno de demostración con acceso a riego.',available=True,rotation=['maiz','haba','papa'],humidity=62,temperature=19),
'p2':dict(id='p2',name='Parcela del Río',community='Zona rural de ejemplo B (no verificada)',lat=-17.620,lon=-66.340,area_ha=2.1,price_bob_month=1100,soil='Franco-arenoso',description='Terreno demostrativo junto a un canal.',available=True,rotation=['papa','quinua','haba'],humidity=54,temperature=18),
'p3':dict(id='p3',name='Parcela del Sol',community='Zona rural de ejemplo C (no verificada)',lat=-17.480,lon=-66.390,area_ha=.9,price_bob_month=620,soil='Franco-arcilloso',description='Terreno de ejemplo con pendiente suave.',available=True,rotation=['maiz','descanso','quinua'],humidity=45,temperature=17)}
class RotationIn(BaseModel):
 rotation:list[str]=Field(min_length=3,max_length=3)
class ChatIn(BaseModel):
 question:str=Field(min_length=1,max_length=1000)
 rotation:list[str]=Field(default_factory=list)
 nasa:dict=Field(default_factory=dict)
def get_sector(id):
 if id not in SECTORS:raise HTTPException(404,'Parcela no encontrada')
 return SECTORS[id]
@router.get('')
def list_sectors():return {'sectors':list(SECTORS.values()),'demo':True,'notice':'Parcelas, precios y comunidades son ficticios'}
@router.get('/{id}')
def sector(id:str):return get_sector(id)
@router.put('/{id}/rotacion')
def update_rotation(id:str,data:RotationIn):
 s=get_sector(id)
 if any(c not in CROPS for c in data.rotation):raise HTTPException(422,'Cultivo no admitido')
 s['rotation']=data.rotation
 return {'ok':True,'rotation':s['rotation'],'persistence':'in-memory demo; resets on restart'}
@router.get('/{id}/nasa')
async def nasa(id:str):
 s=get_sector(id)
 # POWER daily observations are often delayed; use a completed window in the past.
 end=date.today()-timedelta(days=10);start=end-timedelta(days=6)
 try:
  d=await get_power(s['lat'],s['lon'],start.strftime('%Y%m%d'),end.strftime('%Y%m%d'))
  valid=[r for r in d['records'] if isinstance(r.get('T2M'),(float,int)) and isinstance(r.get('PRECTOTCORR'),(float,int))]
  if not valid:return {'status':'unavailable','note':'NASA POWER no devolvió registros válidos para este periodo.'}
  r=valid[-1]
  avg=lambda k:round(sum(x[k] for x in valid if isinstance(x.get(k),(int,float)))/max(1,len([x for x in valid if isinstance(x.get(k),(int,float))])),1)
  return {'status':'live','date':r['date'],'temp':r.get('T2M'),'rain':r.get('PRECTOTCORR'),'humidity':r.get('RH2M'),'temp_avg_7d':avg('T2M'),'rain_total_7d':round(sum(x['PRECTOTCORR'] for x in valid if isinstance(x.get('PRECTOTCORR'),(int,float))),1),'days':len(valid),'source':'NASA POWER','note':'Datos históricos recientes de cuadrícula, NO pronóstico ni medición directa de suelo. No usar como humedad de suelo.'}
 except Exception:
  return {'status':'offline','note':'NASA POWER no respondió. Sin valores ficticios.'}
@router.post('/{id}/asistente')
def assistant(id:str,data:ChatIn):
 s=get_sector(id);q=data.question.lower();rot=data.rotation or s['rotation'];names={'maiz':'maíz','papa':'papa','haba':'haba','quinua':'quinua','descanso':'cobertura vegetal'}
 context=' → '.join(names.get(c,c) for c in rot)
 n=data.nasa; has_nasa=n.get('status')=='live'; climate=(f"NASA POWER: media de {n.get('temp_avg_7d','—')} °C y lluvia acumulada de {n.get('rain_total_7d','—')} mm en {n.get('days','—')} días históricos recientes (hasta {n.get('date')})." if has_nasa else 'NASA POWER no disponible: no se pueden verificar temperatura ni lluvia.')
 if any(x in q for x in ('nasa','lluv','temperat','clima','humedad','sequía','sequia','riego')):
  answer=f"Para {s['name']} ({s['area_ha']} ha, suelo declarado {s['soil']}): {climate} La lluvia regional no mide humedad del suelo. Antes de ajustar riego, verifica humedad con sensor y pronóstico local; POWER histórico no predice el clima futuro."
 elif any(x in q for x in ('cuánt','cuant','surco','espacio','hect','área','area','capacidad','sembradío','sembradio')):
  area=s['area_ha']*10000
  answer=f"{s['name']} tiene {area:,.0f} m² declarados. Si se asignaran 1,2 m² por planta/posición habría un máximo geométrico ilustrativo de {int(area/1.2):,} posiciones, SIN descontar caminos, riego, pendientes ni distancia real de {context}. Para un plan real necesito linderos y marco de siembra por especie."
 elif any(x in q for x in ('rotaci','altern','suelo','sembr','cultivo','haba','maíz','maiz','papa','quinua','fertili','nitrógeno','nitrogeno')):
  answer=f"En {s['name']} ({s['soil']}, {s['area_ha']} ha), propones {context}. Evitar repetir el mismo cultivo consecutivamente puede disminuir la continuidad de algunas plagas. Haba es leguminosa y puede fijar nitrógeno bajo condiciones adecuadas; NO garantiza fertilidad. {climate} Para recomendar fechas y densidades necesito análisis de suelo, agua disponible y calendario local."
 else:
  answer=f"Estoy analizando {s['name']}: {s['area_ha']} ha, suelo declarado {s['soil']}, rotación {context}. {climate} Puedo comparar una secuencia, estimar espacio teórico o explicar qué dato falta para decidir riego y fechas. Soy un asistente contextual basado en reglas, no una IA generativa."
 return {'answer':answer,'type':'rule_based','sector_id':id}
