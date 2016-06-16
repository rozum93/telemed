tekst = open('2_DANE.TXT')
try:
	plik = tekst.read()
finally:
	tekst.close()

print(plik)