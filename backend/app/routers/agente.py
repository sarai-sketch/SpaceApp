from fastapi import APIRouter
from app.models.schemas import ChatInput
from app.agent.agente import explain
router=APIRouter(prefix='/agente',tags=['agente'])
@router.post('/chat')
def chat(data:ChatInput):return explain(data.question,data.scenario)
