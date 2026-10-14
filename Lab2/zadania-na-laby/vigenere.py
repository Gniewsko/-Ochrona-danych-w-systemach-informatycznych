import sys

def encrypt(dane, klucz):
    wynik = bytearray()
    m = len(klucz)
    for i in range(len(dane)):
        wynik.append((dane[i] + klucz[i % m]) % 256)
    return bytes(wynik)

def decrypt(dane, klucz):
    wynik = bytearray()
    m = len(klucz)
    for i in range(len(dane)):
        wynik.append((dane[i] - klucz[i % m]) % 256)
    return bytes(wynik)

if len(sys.argv) < 2:
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    tekst_pl = f.read()

klucz_zamek = b"ZAMEK"
szyfr = encrypt(tekst_pl, klucz_zamek)

with open("vigenere.bin", "wb") as f:
    f.write(szyfr)

assert decrypt(szyfr, klucz_zamek) == tekst_pl
print("zgodnosc: ok")

puste = b""
assert decrypt(encrypt(puste, klucz_zamek), klucz_zamek) == puste

skrajne = bytes(range(256))
assert decrypt(encrypt(skrajne, klucz_zamek), klucz_zamek) == skrajne
print("testy brzegowe: ok")

tekst = b"BRAMABRAMABRAMA"
c_szyfr = encrypt(tekst, b"SZYFR")
c_kod = encrypt(tekst, b"KOD")

print("\nSZYFR:")
print(c_szyfr[0:5].hex(), c_szyfr[5:10].hex(), c_szyfr[10:15].hex())

print("\nKOD:")
print(c_kod[0:5].hex(), c_kod[5:10].hex(), c_kod[10:15].hex())