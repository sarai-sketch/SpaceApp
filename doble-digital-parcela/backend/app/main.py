from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import parcelas,microclima,simulaciones,sensores,agente,sectores
app=FastAPI(title='AGROFLUX · Gemelo Digital Agrícola',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
for router in (parcelas.router,microclima.router,simulaciones.router,sensores.router,agente.router,sectores.router):app.include_router(router,prefix='/api')
@app.get('/health')
def health():return {'ok':True,'mode':'demo+NASA POWER on demand'}
