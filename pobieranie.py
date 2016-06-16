# pobieranie i wyświetlanie pobranych danych
def pobierz():

    cur.execute(
        """
        SELECT pacjent.id,imie,nazwisko,nazwa FROM uczen,klasa
        WHERE uczen.klasa_id=klasa.id
        """)
    uczniowie = cur.fetchall()
    for uczen in uczniowie:
        print uczen['id'], uczen['imie'], uczen['nazwisko'], uczen['nazwa']
    print ""

pobierz()