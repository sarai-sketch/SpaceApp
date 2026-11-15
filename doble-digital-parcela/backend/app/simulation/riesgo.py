def rank_rotation(name: str):
    # Indicadores didácticos, no puntuaciones agronómicas validadas
    values={'Maíz → Maíz':(35,30,25),'Maíz → Leguminosa':(65,70,55),'Maíz → Cobertura → Maíz':(75,85,65)}
    water,soil,cover=values[name]
    return {'name':name,'water_score':water,'soil_score':soil,'cover_score':cover,'evidence':'Comparación cualitativa ilustrativa; requiere calibración local','validated':False}
