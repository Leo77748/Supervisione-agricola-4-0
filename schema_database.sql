CREATE TABLE storico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    modulo TEXT NOT NULL,
    nome TEXT NOT NULL,
    valore REAL NOT NULL,
    unita TEXT,
    stato TEXT
);

CREATE TABLE lavorazioni (
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
);

CREATE TABLE allarmi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    origine TEXT NOT NULL,
    gravita TEXT NOT NULL,
    descrizione TEXT NOT NULL,
    risolto INTEGER DEFAULT 0
);
