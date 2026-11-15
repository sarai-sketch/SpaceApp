def intense_rain(rain_mm:float, hours:float):
    return {'intensity_mm_h':round(rain_mm/max(hours,0.01),2),'warning':'Indicador de intensidad, no pronóstico de inundación.'}
