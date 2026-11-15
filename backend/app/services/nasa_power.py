import httpx
from app.config import POWER_URL

async def get_power(lat:float, lon:float, start:str, end:str):
    params={'parameters':'T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN','community':'AG','longitude':lon,'latitude':lat,'start':start,'end':end,'format':'JSON'}
    async with httpx.AsyncClient(timeout=25) as client:
        response=await client.get(POWER_URL,params=params)
        response.raise_for_status()
        obj=response.json()
    raw=obj.get('properties',{}).get('parameter',{})
    dates=sorted(set().union(*(v.keys() for v in raw.values()))) if raw else []
    records=[]
    for d in dates:
        row={'date':d}
        for key,values in raw.items():
            val=values.get(d)
            row[key]=None if val in (-999,-999.0,None) else val
        records.append(row)
    return {'source':'NASA POWER daily point API','status':'live','lat':lat,'lon':lon,'records':records,'units':'Ver metadatos POWER; radiación ALLSKY_SFC_SW_DWN MJ/m²/día','note':'Punto de cuadrícula, no sensor de parcela'}
