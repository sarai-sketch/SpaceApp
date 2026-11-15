// ESP32: vehículo experimental. NO controla motores sin mecanismos de seguridad.
// Punto de partida para telemetría, sin conducción autónoma ni movimiento.
void setup(){Serial.begin(115200);Serial.println("AGROFLUX autito: modo seguro sin actuadores");}
void loop(){delay(1000);}
