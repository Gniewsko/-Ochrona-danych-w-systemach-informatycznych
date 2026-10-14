tekst = input("Podaj wiadomosc: ")
klucz = input("Podaj klucz tekstowy: ")

# Szyfrowanie
zaszyfrowany = ""
for i in range(len(tekst)):
    przesuniecie = ord(klucz[i % len(klucz)])
    kod = (ord(tekst[i]) + przesuniecie) % 256
    zaszyfrowany += chr(kod)

print("Zaszyfrowany:", repr(zaszyfrowany))

# Odszyfrowanie
odszyfrowany = ""
for i in range(len(zaszyfrowany)):
    przesuniecie = ord(klucz[i % len(klucz)])
    kod = (ord(zaszyfrowany[i]) - przesuniecie) % 256
    odszyfrowany += chr(kod)

print("Odszyfrowany:", odszyfrowany)