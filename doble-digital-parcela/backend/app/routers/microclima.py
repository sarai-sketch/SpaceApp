from fastapi import APIRouter, HTTPException
from app.services.nasa_power import get_power
from app.services.nasa_gpm import CATALOG as GPM
from app.services.nasa_smap import CATALOG as SMAP
from app.services.nasa_srtm import CATALOG as SRTM
router=APIRouter(prefix='/microclima',tags=['microclima'])
@router.get('/catalogo')
def catalog():
 return {'power':{'source':'NASA POWER','status':'live_api','url':'https://power.larc.nasa.gov/'},'gpm':GPM,'smap':SMAP,'srtm':SRTM,'other_sources':['https://earthexplorer.usgs.gov/','https://lpdaac.usgs.gov/products/','https://search.earthdata.nasa.gov/search?q=VIIRS','https://dataspace.copernicus.eu/','https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels','https://ecostress.jpl.nasa.gov/data','https://gaez.fao.org/']}
@router.get('/power')
async def power(lat:float=-17.39,lon:float=-66.16,start:str='20261001',end:str='20261007'):
 try:return await get_power(lat,lon,start,end)
 except Exception as e:raise HTTPException(502,detail=f'NASA POWER no disponible: {type(e).__name__}')
