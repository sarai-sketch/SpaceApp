from fastapi import APIRouter, HTTPException
from app.models.schemas import Scenario
from app.simulation.water import simulate
from app.simulation.riesgo import rank_rotation
router=APIRouter(prefix='/simulaciones',tags=['simulaciones'])
@router.post('/ejecutar')
def run(s:Scenario):
 try:return simulate(s)
 except ValueError as e:raise HTTPException(422,detail=str(e))
@router.get('/rotaciones')
def rotations():return {'strategies':[rank_rotation(n) for n in ['Maíz → Maíz','Maíz → Leguminosa','Maíz → Cobertura → Maíz']],'disclaimer':'Indicadores conceptuales, no predicción de rendimientos ni consejo de siembra.'}
