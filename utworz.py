# tworzenie tabel
cur.execute("DROP TABLE IF EXISTS czynnosc;")

cur.execute("""
    CREATE TABLE IF NOT EXISTS czynnosc (
        id INTEGER PRIMARY KEY ASC,
        nazwa varchar(250) NOT NULL,
        profil varchar(250) DEFAULT ''
    )""")

cur.executescript("""
    DROP TABLE IF EXISTS pacjent;
    CREATE TABLE IF NOT EXISTS pacjent (
        id INTEGER PRIMARY KEY ASC,
        imie varchar(250) NOT NULL,
        nazwisko varchar(250) NOT NULL,
        czynnosc_id INTEGER NOT NULL,
        FOREIGN KEY(pacjent_id) REFERENCES czynnosc(id)
    )""")