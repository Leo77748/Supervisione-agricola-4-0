import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

TOPICS = {
    "meteo": "azienda/campi/meteo",
    "irrigazione": "azienda/irrigazione/rotolone1",
    "mezzi": "azienda/mezzi/gps",
    "biogas": "azienda/biogas/digestore"
}

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT, 60)
    print("Simulatore MQTT avviato. Premi CTRL+C per fermare.")
    while True:
        pacchetti = {
            "meteo": {
                "timestamp": datetime.now().isoformat(),
                "campo": "Campo Nord",
                "temperatura_aria": round(random.uniform(15, 30), 1),
                "umidita_terreno": round(random.uniform(15, 55), 1),
                "batteria": random.randint(50, 100)
            },
            "irrigazione": {
                "timestamp": datetime.now().isoformat(),
                "irrigatore": "Rotolone 1",
                "pressione_bar": round(random.uniform(2.0, 5.5), 1),
                "portata_l_min": random.randint(120, 240),
                "avanzamento_percento": random.randint(0, 100)
            },
            "mezzi": {
                "timestamp": datetime.now().isoformat(),
                "mezzo": "Deutz 5075D",
                "lat": round(46.300 + random.uniform(-0.002, 0.002), 6),
                "lon": round(9.050 + random.uniform(-0.002, 0.002), 6),
                "velocita_kmh": round(random.uniform(0, 18), 1),
                "gasolio_percento": random.randint(10, 100)
            },
            "biogas": {
                "timestamp": datetime.now().isoformat(),
                "temperatura_digestore": round(random.uniform(36, 42), 1),
                "pressione_mbar": round(random.uniform(70, 125), 1),
                "energia_kwh": random.randint(2500, 3800)
            }
        }
        for nome, payload in pacchetti.items():
            client.publish(TOPICS[nome], json.dumps(payload))
            print(f"Inviato su {TOPICS[nome]}: {payload}")
        time.sleep(5)

if __name__ == "__main__":
    main()
