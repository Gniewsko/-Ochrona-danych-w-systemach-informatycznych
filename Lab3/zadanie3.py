import math
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def oblicz_entropie(dane):
    licz = {}
    for b in dane:
        if b in licz:
            licz[b] = licz[b] + 1
        else:
            licz[b] = 1
    
    h = 0.0
    dlugosc = len(dane)
    for b in licz:
        p = licz[b] / dlugosc
        h = h - (p * math.log2(p))
    return h

znaki = "abcdefghijklmnopqrstuvwxyz0123456789"

f = open("slaby_ecb.bin", "rb")
caly_kryp = f.read()
f.close()

probka = caly_kryp[:4096]

kandy = []
for z in znaki:
    klucz = (z * 16).encode("ascii")
    szyfr_ecb = AES.new(klucz, AES.MODE_ECB)
    odzy_probka = szyfr_ecb.decrypt(probka)
    h = oblicz_entropie(odzy_probka)
    kandy.append((h, z, klucz))

kandy.sort()

print("5 najlepszych kandydatow:")
for i in range(5):
    h, z, k = kandy[i]
    print("znak:", z, "entropia H:", round(h, 4))

naj_klucz = kandy[0][2]
deszyfr_ecb = AES.new(naj_klucz, AES.MODE_ECB)
odzy_caly = deszyfr_ecb.decrypt(caly_kryp)
tekst = unpad(odzy_caly, 16)

tekst_jawny = tekst.decode("utf-8")
linie = tekst_jawny.split("\n")
print("pierwszy wiersz tekstu:", linie[0])