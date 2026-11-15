# AGROFLUX — Gemelo Digital Agrícola 🌱🛰️

Prototipo funcional de hackathon inspirado en el panel oscuro y la parcela 3D de la referencia del equipo. Incluye React + Three.js, FastAPI, balance hídrico simplificado, escenarios de lluvia y temperatura, NASA POWER real bajo demanda, tres rotaciones ilustrativas, asistente explicativo local y plantillas ESP32.

**IMPORTANTE:** es un MVP de investigación, no un predictor de rendimiento, ni un sistema de protección de cultivos validado. La vista 3D es esquemática. El único conector NASA que consulta una API directamente es **NASA POWER**; las demás fuentes están catalogadas para futuras integraciones. Los datos iniciales y la parcela son ficticios.

## Requisitos
- Node.js 20+ y npm
- Python 3.10+
- Conexión a Internet para instalar dependencias y consultar NASA POWER

## 1. Iniciar backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Documentación interactiva: http://localhost:8000/docs

## 2. Iniciar frontend (otra terminal)
```bash
cd frontend
npm install
npm run dev
```
Abrir **http://localhost:5173**.

## 3. Usar
1. Gira y acerca la parcela 3D con el mouse.
2. Ajusta lluvia +40 %, temperatura −8 °C, 3 días.
3. Pulsa **Ejecutar simulación**; se calculan indicadores en FastAPI.
4. Pulsa **NASA POWER** para obtener una muestra histórica real de octubre de 2026 para las coordenadas de demostración; luego ejecuta otra simulación. Si la fuente no responde, conserva el escenario hipotético.
5. En **Rotaciones** compara tres opciones **ilustrativas**.
6. Pregunta al asistente: devuelve una explicación basada en reglas, no una IA generativa.

## 4. Pruebas
```bash
cd backend
python -m pytest -q
```

## 5. Compilar frontend
```bash
cd frontend
npm run build
```

## 6. Datos y licencias
NASA POWER: https://power.larc.nasa.gov/ . GPM: https://gpm.nasa.gov/data . SMAP, SRTM, Landsat/USGS, VIIRS, LP DAAC, Copernicus, ERA5, ECOSTRESS y FAO GAEZ aparecen en `GET /api/microclima/catalogo`. Revisar requisitos de Earthdata Login, cuotas, cobertura, licencias y resoluciones antes de integrar.

## 7. Modelo
- `TAW = 1000*(FC-WP)*Zr`
- `RAW = p*TAW`
- `Ks = 1` si agotamiento `Dr <= RAW`, de lo contrario `(TAW-Dr)/(TAW-RAW)` acotado a `[0,1]`.
- `ETa = Ks*Kc*ET0`
- `Dr_next = clamp(Dr + ETa + runoff - rain - irrigation + drainage, 0, TAW)`.
- `runoff = rain*runoff_fraction` es una simplificación didáctica.
- Si la precipitación sobrepasa la capacidad de almacenamiento, se contabiliza drenaje instantáneo.
- La temperatura se muestra como **media** desplazada, no determina automáticamente daño por helada.

## Estructura
`backend/` API y modelos; `frontend/` interfaz 3D; `hardware/` firmware demostrativo; `data/` datos sintéticos; `docs/` arquitectura y limitaciones.

## Próximas fases
1. GeoJSON y parcelas reales con permisos.
2. GPM IMERG, SMAP y DEM SRTM mediante Earthdata autenticado, reproyección y QA.
3. Datos horarios, Penman–Monteith, infiltración física y umbrales por fenología.
4. Modelos de rotación y suelo validados con especialistas.
5. Agente LLM con recuperación de fuentes, auditoría y límites de seguridad.
6. Autenticación, persistencia PostgreSQL/PostGIS y telemetría real.

## Nota de seguridad
No exponer endpoints de sensores sin autenticación. No utilizar el sistema como única base para decisiones agronómicas, protección frente a heladas o emergencias. No fabricar sondas de neutrones ni usar fuentes radiactivas.
