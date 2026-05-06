/*
Esempio ESP32 MQTT dimostrativo.
Per maturità puoi dire: nella versione reale l'ESP32 invia questi dati al PC centrale via Wi-Fi/MQTT.
Richiede librerie WiFi.h e PubSubClient.
*/
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "NOME_WIFI";
const char* password = "PASSWORD_WIFI";
const char* mqtt_server = "IP_PC_CENTRALE";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void reconnect() {
  while (!client.connected()) {
    client.connect("ESP32_CAMPO_1");
    delay(500);
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temperatura = 22.5;
  float umiditaTerreno = 38.0;

  String payload = "{";
  payload += "\"campo\":\"Campo Nord\",";
  payload += "\"temperatura\":" + String(temperatura) + ",";
  payload += "\"umidita_terreno\":" + String(umiditaTerreno);
  payload += "}";

  client.publish("azienda/campi/meteo", payload.c_str());
  delay(5000);
}
