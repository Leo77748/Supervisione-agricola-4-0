import sqlite3
from datetime import datetime
from pathlib import Path

DB_NAME = "azienda_agricola.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def crea_database():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS storico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        modulo TEXT NOT NULL,
        nome TEXT NOT NULL,
        valore REAL NOT NULL,
        unita TEXT,
        stato TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS lavorazioni (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        campo TEXT NOT NULL,
        lavorazione TEXT NOT NULL,
        mezzo TEXT NOT NULL,
        attrezzo TEXT,
        ore REAL,
        gasolio REAL,
        superficie REAL,
        stato TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS allarmi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        origine TEXT NOT NULL,
        gravita TEXT NOT NULL,
        descrizione TEXT NOT NULL,
        risolto INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def inserisci_storico(modulo, nome, valore, unita, stato="OK"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO storico (data, modulo, nome, valore, unita, stato)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), modulo, nome, float(valore), unita, stato))
    conn.commit()
    conn.close()

def inserisci_lavorazione(campo, lavorazione, mezzo, attrezzo, ore, gasolio, superficie, stato):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO lavorazioni (data, campo, lavorazione, mezzo, attrezzo, ore, gasolio, superficie, stato)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), campo, lavorazione, mezzo, attrezzo, float(ore), float(gasolio), float(superficie), stato))
    conn.commit()
    conn.close()

def inserisci_allarme(origine, gravita, descrizione):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO allarmi (data, origine, gravita, descrizione, risolto)
    VALUES (?, ?, ?, ?, 0)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), origine, gravita, descrizione))
    conn.commit()
    conn.close()

def leggi_tabella(nome_tabella):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {nome_tabella} ORDER BY id DESC")
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        return cols, rows
    finally:
        conn.close()
