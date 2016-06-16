# wstawiamy jeden rekord danych
cur.execute('INSERT INTO czynnosc VALUES(NULL, ?, ?);', ('1', 'bieg'))
cur.execute('INSERT INTO czynnosc VALUES(NULL, ?, ?);', ('2', 'ćwiczenia'))

# zapytanie
cur.execute('SELECT id FROM czynnosc WHERE nazwa = ?', ('1',))
czynnosc_id = cur.fetchone()[0]

uczniowie = (
    (None, 'Tomasz', 'Nowak', czynnosc_id),
    (None, 'Jan', 'Kos', czynnosc_id),
    (None, 'Piotr', 'Kowalski', czynnosc_id)
)

# wstawiamy wiele rekordów
cur.executemany('INSERT INTO pacjent VALUES(?,?,?,?)', pacjenci)

# zatwierdzamy zmiany w bazie
con.commit()