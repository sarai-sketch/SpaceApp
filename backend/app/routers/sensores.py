from fastapi import APIRouter
from app.models.schemas import SensorReading
from app.db.store import SENSOR_READINGS
router=APIRouter(prefix='/sensores',tags=['sensores'])
@router.post('/lecturas')
def ingest(data:SensorReading):
 SENSOR_READINGS.append(data.model_dump())
 return {'ok':True,'count':len(SENSOR_READINGS),'storage':'memoria temporal; sin autenticación, solo desarrollo'}
@router.get('/lecturas')
def read():return list(SENSOR_READINGS)
