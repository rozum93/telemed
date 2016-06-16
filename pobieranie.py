# pobieranie i wyświetlanie pobranych danych
def pobierz():

    cur.execute(
        """
        SELECT pacjent.id,imie,nazwisko,nazwa FROM pacjent, czynnosc
        WHERE pacjent.czynnosc_id=czynnosc.id
        """)
    pacjenci = cur.fetchall()
    for pacjent in pacjenci:
        print(pacjent['id'], pacjent['imie'], pacjent['nazwisko'], pacjent['nazwa'])
    print("")

pobierz()