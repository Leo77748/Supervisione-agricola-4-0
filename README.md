# Supervisione Agricola 4.0

Cartella pronta per simulare su PC centrale una dashboard agricola 4.0 per maturità.

## Cosa contiene

- `app.py`: dashboard Streamlit da aprire nel browser.
- `database.py`: funzioni SQLite per salvare storico, lavorazioni e allarmi.
- `azienda_agricola.db`: viene creato automaticamente al primo avvio.
- `mqtt_simulator.py`: simulatore IoT MQTT facoltativo.
- `schema_database.sql`: schema tabelle.
- `schema_node_red.txt`: schema logico per spiegare Node-RED.
- `esp32_mqtt_example.ino`: esempio per dire come sarebbe collegato un ESP32 reale.

## Installazione veloce

1. Installa Python 3.10 o superiore.
2. Durante l’installazione spunta: Add Python to PATH.
3. Installa Visual Studio Code.
4. Apri Visual Studio Code.
5. Vai su File -> Apri cartella.
6. Seleziona la cartella `supervisione_agricola_4_0`.
7. Apri il terminale di VS Code con CTRL + ò.
8. Scrivi:

```bash
pip install -r requirements.txt
```

## Avvio del programma

Nel terminale scrivi:

```bash
streamlit run app.py
```

Si apre Chrome/Edge con la dashboard.

## Come farlo vedere alla commissione

1. Collega il PC al monitor grande.
2. Imposta schermo duplicato o esteso.
3. Apri la dashboard.
4. Premi F11 per schermo intero.
5. Apri la sezione Dashboard generale.
6. Premi "Carica dati demo".
7. Mostra:
   - mappa mezzi GPS simulata
   - grafici meteo e irrigazione
   - inserimento dati da tastiera
   - storico e grafici
   - report CSV
   - allarmi

## Memorizzazione processo

La memorizzazione avviene nel file `azienda_agricola.db`.

Quando inserisci:
- un dato sensore
- una lavorazione agricola
- un allarme

il programma salva una riga nel database SQLite.

Percorso dimostrativo:
1. Vai in `Inserimento dati`.
2. Inserisci temperatura, pressione o gasolio.
3. Premi salva.
4. Vai in `Storico e grafici`.
5. Fai vedere che il dato è rimasto salvato.
6. Chiudi e riapri il programma.
7. Il dato è ancora presente: questo dimostra lo storico.

## Frase pronta da dire all’esame

Questa è una simulazione funzionante su PC. I dati vengono inseriti da tastiera o generati in modo simulato, ma la struttura è uguale a un impianto reale. In un sistema vero i dati arriverebbero da sensori, PLC, centraline, GPS, robot di stalla e app dei mezzi agricoli. Il PC centrale li riceve, li visualizza e li memorizza in un database storico.

## MQTT facoltativo

Serve solo se installi Mosquitto MQTT Broker.

Terminale 1:
```bash
streamlit run app.py
```

Terminale 2:
```bash
python mqtt_simulator.py
```

La dashboard funziona anche senza MQTT.
