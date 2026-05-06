import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import random
from datetime import datetime
from database import crea_database, inserisci_storico, inserisci_lavorazione, inserisci_allarme, DB_NAME

st.set_page_config(page_title="Supervisione Agricola 4.0", page_icon="🚜", layout="wide")
crea_database()

def leggi_tabella(nome_tabella):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(f"SELECT * FROM {nome_tabella} ORDER BY id DESC", conn)
    conn.close()
    return df

def seed_demo():
    for i in range(1, 21):
        inserisci_storico("Meteo", f"Campo {i} temperatura", random.randint(18, 28), "°C", "OK")
        inserisci_storico("Irrigazione", f"Rotolone {i} pressione", round(random.uniform(3.0, 6.0), 1), "bar", "OK")
    inserisci_lavorazione("Campo Nord", "Aratura", "Deutz 5075D", "Aratro", 4, 25, 12, "Completata")
    inserisci_lavorazione("Campo Sud", "Semina", "Goldoni Ronin 50", "Seminatrice", 3, 15, 8, "In corso")
    inserisci_allarme("Irrigazione", "2 - Attenzione", "Pressione bassa rotolone Campo Basso")
    inserisci_allarme("Biogas", "3 - Critico", "Temperatura digestore alta")

campi = pd.DataFrame({
    "Campo":["Campo Nord","Campo Sud","Campo Est","Campo Ovest","Campo Alto","Campo Basso","Campo Bosco","Campo Fieno1","Campo Fieno2","Campo Irr1"],
    "Superficie_ha":[12,8,15,10,6,9,20,7,11,14],
    "Coltura":["Mais","Frumento","Erba medica","Orzo","Vigneto","Mais","Bosco","Prato","Prato","Mais"],
    "Comune":["Trento","Rovereto","Riva del Garda","Arco","Pergine","Lavis","Mezzolombardo","Cles","Tione","Predazzo"],
    "Lat":[46.30,46.28,46.31,46.29,46.32,46.27,46.33,46.30,46.31,46.29],
    "Lon":[9.05,9.07,9.10,9.00,9.08,9.06,9.12,9.04,9.03,9.06]
})
mezzi = pd.DataFrame({
    "Mezzo":["Deutz 5075D","Goldoni Ronin 50","Mietitrebbia","Iveco Daily","Deutz 6150","Carraro TTR","Telescopico"],
    "Ore":[3200,2100,1500,900,4000,1800,1200],
    "Velocità_kmh":[12,8,6,50,10,7,5],
    "Gasolio_%":[60,70,80,50,65,75,70],
    "Stato":["Lavoro","Attivo","Raccolta","Trasporto","Lavoro","Lavoro","Carico"],
    "Lat":[46.30,46.31,46.28,46.29,46.32,46.30,46.31],
    "Lon":[9.05,9.06,9.07,9.06,9.08,9.03,9.07]
})
robot = pd.DataFrame({
    "Robot":["Mungitura 1","Spingiforaggio 1","Pulizia 1","Alimentatore 1","Vitelli 1"],
    "Stato":["Attivo","Attivo","Fermo","Attivo","Attivo"],
    "Batteria_%":[80,60,30,70,65],
    "Attività":["Mungitura","Giro","Ricarica","Distribuzione","Alimentazione"],
    "Errori":[0,1,0,0,0]
})

st.sidebar.title("AgroControl 4.0")
menu = st.sidebar.radio("Menu", ["Dashboard generale","Inserimento dati","Campi e meteo","Irrigazione","Mezzi e GPS","Stalla e robot","Allarmi","Storico e grafici","Report"])
if st.sidebar.button("Carica dati demo"):
    seed_demo()
    st.sidebar.success("Dati demo caricati")

st.title("Supervisione Agricola 4.0 - PC Centrale")
st.caption("Simulazione funzionante su PC: dati inseriti da tastiera, database SQLite e dashboard per monitor grande.")

storico = leggi_tabella("storico")
lavorazioni = leggi_tabella("lavorazioni")
allarmi = leggi_tabella("allarmi")

if menu == "Dashboard generale":
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Dati salvati", len(storico))
    c2.metric("Lavorazioni", len(lavorazioni))
    c3.metric("Allarmi", len(allarmi))
    c4.metric("Moduli", "8")
    st.subheader("Stato generale")
    stato = pd.DataFrame({
        "Modulo":["Meteo","Irrigazione","Lavorazioni","Mezzi GPS","Stalla","Robot","Biogas","Database"],
        "Stato":["OK","Attivo","Operativo","GPS simulato","OK","OK","Attenzione","SQLite attivo"],
        "Descrizione":["Campi e clima","Acqua e pressione","Ore e gasolio","Mappa mezzi","Animali e ambiente","Mungitura/alimentazione","Energia e digestore","Memorizzazione processo"]
    })
    st.dataframe(stato, use_container_width=True)
    st.map(mezzi.rename(columns={"Lat":"lat","Lon":"lon"})[["lat","lon"]])
    if not allarmi.empty:
        st.warning("Allarmi presenti")
        st.dataframe(allarmi.head(5), use_container_width=True)

elif menu == "Inserimento dati":
    st.header("Inserimento e memorizzazione processo")
    tab1, tab2, tab3 = st.tabs(["Dato sensore", "Lavorazione", "Allarme"])
    with tab1:
        with st.form("storico"):
            modulo = st.selectbox("Modulo", ["Meteo","Irrigazione","Stalla","Robot","Biogas","Mezzi"])
            nome = st.text_input("Nome dato", "Temperatura Campo Nord")
            valore = st.number_input("Valore", value=22.0)
            unita = st.text_input("Unità", "°C")
            stato = st.selectbox("Stato", ["OK","ATTENZIONE","ALLARME CRITICO"])
            if st.form_submit_button("Salva dato nello storico"):
                inserisci_storico(modulo, nome, valore, unita, stato)
                st.success("Dato salvato nel database azienda_agricola.db")
    with tab2:
        with st.form("lav"):
            campo = st.text_input("Campo", "Campo Nord")
            lavorazione = st.selectbox("Lavorazione", ["Aratura","Semina","Raccolta","Fienagione","Trattamento","Trasporto"])
            mezzo = st.text_input("Mezzo", "Deutz 5075D")
            attrezzo = st.text_input("Attrezzo", "Aratro")
            ore = st.number_input("Ore lavoro", value=4.0)
            gasolio = st.number_input("Gasolio [L]", value=25.0)
            superficie = st.number_input("Superficie [ha]", value=12.0)
            stato_lav = st.selectbox("Stato lavorazione", ["In corso","Completata","Sospesa"])
            if st.form_submit_button("Memorizza lavorazione"):
                inserisci_lavorazione(campo, lavorazione, mezzo, attrezzo, ore, gasolio, superficie, stato_lav)
                st.success("Lavorazione memorizzata nello storico")
    with tab3:
        with st.form("all"):
            origine = st.selectbox("Origine", ["Irrigazione","Biogas","Stalla","Mezzi","Robot"])
            gravita = st.selectbox("Gravità", ["1 - Avviso","2 - Attenzione","3 - Critico"])
            descrizione = st.text_input("Descrizione", "Pressione bassa")
            if st.form_submit_button("Registra allarme"):
                inserisci_allarme(origine, gravita, descrizione)
                st.success("Allarme registrato")

elif menu == "Campi e meteo":
    st.header("Campi e meteo")
    meteo = campi.copy()
    meteo["Temperatura_aria_C"] = [random.randint(18,28) for _ in range(len(meteo))]
    meteo["Umidità_suolo_%"] = [random.randint(35,70) for _ in range(len(meteo))]
    st.dataframe(meteo, use_container_width=True)
    st.plotly_chart(px.bar(meteo, x="Campo", y="Umidità_suolo_%", title="Umidità terreno simulata"), use_container_width=True)

elif menu == "Irrigazione":
    st.header("Irrigazione")
    irr = pd.DataFrame({
        "Irrigatore":["Rotolone 1","Pivot 1","Lineare 1","Rotolone 2","Pivot 2"],
        "Campo":["Campo Nord","Campo Est","Campo Sud","Campo Ovest","Campo Irr1"],
        "Acqua_m3":[120,500,300,150,450],
        "Pressione_bar":[6,5,4,5,5],
        "Tempo_min":[90,180,120,100,170],
        "Stato":["Attivo","Attivo","Fermo","Attivo","Attivo"]
    })
    st.dataframe(irr, use_container_width=True)
    st.plotly_chart(px.pie(irr, names="Campo", values="Acqua_m3", title="Acqua distribuita per campo"), use_container_width=True)

elif menu == "Mezzi e GPS":
    st.header("Mezzi agricoli e posizione GPS simulata")
    st.dataframe(mezzi, use_container_width=True)
    st.map(mezzi.rename(columns={"Lat":"lat","Lon":"lon"})[["lat","lon"]])
    st.plotly_chart(px.bar(mezzi, x="Mezzo", y="Gasolio_%", title="Livello gasolio mezzi"), use_container_width=True)

elif menu == "Stalla e robot":
    st.header("Stalla e robot")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Animali presenti", 250)
    c2.metric("Animali munti", 185)
    c3.metric("Latte giornaliero [L]", 6200)
    c4.metric("Robot attivi", 4)
    st.dataframe(robot, use_container_width=True)
    st.plotly_chart(px.bar(robot, x="Robot", y="Batteria_%", title="Batteria robot"), use_container_width=True)

elif menu == "Allarmi":
    st.header("Registro allarmi")
    if allarmi.empty:
        st.info("Nessun allarme registrato. Inseriscine uno nella sezione 'Inserimento dati'.")
    else:
        st.dataframe(allarmi, use_container_width=True)

elif menu == "Storico e grafici":
    st.header("Storico dati salvati")
    if storico.empty:
        st.info("Storico vuoto. Usa 'Carica dati demo' o inserisci dati da tastiera.")
    else:
        st.dataframe(storico, use_container_width=True)
        st.plotly_chart(px.line(storico.sort_values("id"), x="data", y="valore", color="modulo", title="Andamento valori memorizzati"), use_container_width=True)

elif menu == "Report":
    st.header("Report e esportazione")
    st.write("Qui puoi dimostrare che il processo viene memorizzato in SQLite.")
    st.dataframe(lavorazioni, use_container_width=True)
    csv = lavorazioni.to_csv(index=False).encode("utf-8")
    st.download_button("Scarica report lavorazioni CSV", csv, "report_lavorazioni.csv", "text/csv")
