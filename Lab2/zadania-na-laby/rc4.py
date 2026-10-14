import sys
import math
import time
import itertools
import string

def rc4(dane, klucz):
    S = list(range(256))
    j = 0
    m = len(klucz)
    for i in range(256):
        j = (j + S[i] + klucz[i % m]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    wynik = bytearray()
    for b in dane:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        wynik.append(b ^ S[(S[i] + S[j]) % 256])
    return bytes(wynik)

def entropia(dane):
    stat = {}
    for b in dane:
        stat[b] = stat.get(b, 0) + 1
    n = len(dane)
    h = 0.0
    for c in stat.values():
        p = c / n
        h -= p * math.log2(p)
    return h

if len(sys.argv) < 2:
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    kryptogram = f.read()

assert rc4(rc4(b"test", b"abc"), b"abc") == b"test"
print("test ok")

probka = kryptogram[:512]
litery = string.ascii_lowercase.encode("ascii")
wszystkie = len(litery) ** 3

start = time.perf_counter()
ranking = []
for k in itertools.product(litery, repeat=3):
    klucz = bytes(k)
    tekst = rc4(probka, klucz)
    ranking.append((entropia(tekst), klucz))
czas = time.perf_counter() - start

ranking.sort(key=lambda x: (x[0], x[1]))

print("\nTOP 5:")
for i in range(5):
    h, k = ranking[i]
    print(f"{i+1}. klucz: {k.decode()} | h: {h:.4f}")

wybrany = ranking[0][1]
odszyfrowany = rc4(kryptogram, wybrany)

with open("rc4.txt", "wb") as f:
    f.write(odszyfrowany)

assert rc4(odszyfrowany, wybrany) == kryptogram
print("ponowne szyfr ok")

print(f"klucz: {wybrany.decode()}")
print(f"proby: {wszystkie}")
print(f"czas: {czas:.3f} s")
print(f"h kryptogramu: {entropia(kryptogram):.4f}")
print(f"h tekstu: {entropia(odszyfrowany):.4f}")
print("zapisano plik")