from app.agent.tools import scenario_summary

def explain(question, scenario):
    if scenario:
        summary=scenario_summary(scenario)
        return {'mode':'local_explainable','answer':f"Según el modelo ilustrativo, el agua disponible al final sería {summary['available_water_mm']} mm y el riesgo hídrico es {summary['water_risk']}. Riesgo térmico: {summary['cold_risk']}. No es un pronóstico ni una estimación validada de pérdidas. Para decidir medidas, confirme datos del terreno y consulte asesoría agronómica.",'model_output':summary,'disclaimer':'Asistente local basado en reglas, no modelo generativo. No hay conexión con institución externa.'}
    return {'mode':'local_explainable','answer':'Puedes consultar el escenario, comparar rotaciones o conectar NASA POWER. Las recomendaciones requieren datos reales y validación agronómica.'}