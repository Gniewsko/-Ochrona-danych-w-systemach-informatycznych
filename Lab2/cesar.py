tekst = input("Podaj wiadomosc: ")
k = int(input("Podaj klucz (liczba): "))

# Szyfrowanie
zaszyfrowany = ""
for znak in tekst:
    kod = (ord(znak) + k) % 256
    zaszyfrowany += chr(kod)

print("Zaszyfrowany:", repr(zaszyfrowany))

# Odszyfrowanie
odszyfrowany = ""
for znak in zaszyfrowany:
    kod = (ord(znak) - k) % 256
    odszyfrowany += chr(kod)

print("Odszyfrowany:", odszyfrowany)