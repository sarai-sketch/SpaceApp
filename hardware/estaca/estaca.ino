// ESP32 - plantilla de demostración, NO sensor físico calibrado.
// Configura WiFi, endpoint y sensores reales antes de uso en campo.
#include <WiFi.h>
#include <HTTPClient.h>
const char* WIFI_SSID = "TU_WIFI";
const char* WIFI_PASS = "TU_CLAVE";
const char* API_URL = "http://192.168.1.100:8000/api/sensores/lecturas";
void setup(){Serial.begin(115200);WiFi.begin(WIFI_SSID,WIFI_PASS);}
void loop(){
  if(WiFi.status()==WL_CONNECTED){
    // VALORES SINTÉTICOS: sustituir por lecturas ADC + calibración de sensores
    float temperature_c=18.5;
    float moisture_pct=35.0;
    HTTPClient http;http.begin(API_URL);http.addHeader("Content-Type","application/json");
    String payload=String("{\"device_id\":\"estaca-demo\",\"temperature_c\":")+String(temperature_c)+String(",\"moisture_pct\":")+String(moisture_pct)+String("}");
    int code=http.POST(payload);Serial.printf("HTTP %d\n",code);http.end();
  }
  delay(60000);
}
