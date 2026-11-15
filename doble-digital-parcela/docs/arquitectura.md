# Arquitectura técnica
React/Three.js → FastAPI → modelo hídrico de depósito único y fuentes de datos.

- `POST /api/simulaciones/ejecutar`: ejecuta modelo diario.
- `GET /api/microclima/power`: llama NASA POWER en tiempo real; puede fallar por red o disponibilidad.
- `GET /api/microclima/catalogo`: catálogo de otras fuentes. **No** implica integración activa.
- `POST /api/agente/chat`: asistente local basado en reglas; no IA generativa conectada.
- `POST /api/sensores/lecturas`: recibe datos ESP32 en memoria; no es persistente ni autenticado.
- `GET /api/simulaciones/rotaciones`: tres estrategias y puntuaciones ilustrativas, no científicamente validadas.

## Limitaciones
La imagen 3D es conceptual y no reproduce el perímetro real de una finca. No hay simulación física de granizo, congelamiento, crecimiento ni daños económicos. Las imágenes Landsat/VIIRS, GPM, SMAP, SRTM, Copernicus, ERA5, ECOSTRESS y GAEZ están documentadas como fuentes futuras; no se descargan automáticamente. Para datos NASA POWER, usar coordenadas, fechas y unidades adecuadas. El modelo de escorrentía es una fracción arbitraria elegida por el usuario, no un modelo de inundación. Para uso operativo se necesitan validación, calibración, controles de acceso y privacidad.
