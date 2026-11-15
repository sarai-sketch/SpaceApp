from app.models.schemas import Scenario

def simulate(s: Scenario) -> dict:
    if s.field_capacity <= s.wilting_point:
        raise ValueError('Capacidad de campo debe superar punto de marchitez')
    if not (s.wilting_point <= s.soil_moisture <= s.field_capacity):
        raise ValueError('Humedad inicial debe estar entre marchitez y capacidad de campo')
    taw = 1000 * (s.field_capacity - s.wilting_point) * s.root_depth_m
    raw = s.p_fraction * taw
    depletion = 1000 * (s.field_capacity - s.soil_moisture) * s.root_depth_m
    daily = []
    for d in range(1, s.duration_days + 1):
        rain = s.baseline_rain_mm_day * (1 + s.rain_change_pct / 100)
        runoff = rain * s.runoff_fraction
        available_rain = rain - runoff
        ks = 1 if depletion <= raw else max(0, min(1, (taw-depletion)/(taw-raw)))
        eta = ks * s.kc * s.eto_mm_day
        net = available_rain + s.irrigation_mm_day - eta
        new_depletion = depletion - net
        drainage = max(0, -new_depletion)
        depletion = max(0, min(taw, new_depletion))
        moisture = s.field_capacity - depletion / (1000*s.root_depth_m)
        # Indicador térmico preliminar: media no permite inferir horas de helada
        temp = s.baseline_temp_c + s.temp_delta_c
        daily.append(dict(day=d, rain_mm=round(rain,3), runoff_mm=round(runoff,3), eta_mm=round(eta,3), drainage_mm=round(drainage,3), depletion_mm=round(depletion,3), moisture_pct=round(100*moisture,2), temp_mean_c=round(temp,2), water_stress=round(1-ks,3)))
    final=daily[-1]
    risk = 'alto' if final['depletion_mm'] > raw else 'moderado' if final['depletion_mm'] > .75*raw else 'bajo'
    cold = 'posible, requiere temperaturas mínimas horarias' if final['temp_mean_c'] <= 8 else 'no descartado sin datos horarios'
    return {'daily':daily,'summary':{'water_risk':risk,'cold_risk':cold,'available_water_mm':round(taw-final['depletion_mm'],2),'taw_mm':round(taw,2),'raw_mm':round(raw,2),'final_moisture_pct':final['moisture_pct'],'rain_total_mm':round(sum(x['rain_mm'] for x in daily),2),'final_temp_mean_c':final['temp_mean_c']},'assumptions':['Modelo de depósito único FAO-56 simplificado','Escorrentía fraccional de demostración, no hidrología de inundaciones','ET0 constante durante el escenario; cambiar temperatura no recalcula ET0','Sin ascenso capilar; drenaje instantáneo sobre capacidad de campo','Riesgo térmico cualitativo: no estima daño ni rendimiento','Escenario hipotético, no pronóstico meteorológico']}
