from fastapi import APIRouter
from app.db.store import PARCELS
router=APIRouter(prefix='/parcelas',tags=['parcelas'])
@router.get('')
def list_parcels():return PARCELS
@router.get('/{id}')
def parcel(id:str):return next((p for p in PARCELS if p['id']==id),{'error':'no encontrada'})
