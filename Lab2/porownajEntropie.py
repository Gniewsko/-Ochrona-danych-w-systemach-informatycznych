import math
import os


def oblicz_entropie(dane: bytes) -> float:
    if not dane:
        return 0.0
    stat = {}
    for b in dane:
        stat[b] = stat.get(b, 0) + 1

    n = len(dane)
    h = 0.0
    for ilosc in stat.values():
        p = ilosc / n
        h -= p * math.log2(p)
    return h


# Lista plików laboratoryjnych do zestawienia
pliki = [
    ("1918_1.3_sample.txt", "Tekst naturalny (korpus)"),
    ("crypto.rot", "Szyfr Cezara"),
    ("crypto.rc4", "Szyfr strumieniowy RC4"),
    ("encrypted.3rc4", "Szyfr strumieniowy RC4"),
]

katalog = os.path.dirname(os.path.abspath(__file__))

print(f"{'Plik':<25} | {'Typ':<24} | {'Entropia [b/B]':<14}")
print("-" * 70)

for nazwa, opis in pliki:
    sciezka = os.path.join(katalog, nazwa)
    if os.path.exists(sciezka):
        with open(sciezka, "rb") as f:
            dane = f.read()
        h = oblicz_entropie(dane)
        print(f"{nazwa:<25} | {opis:<24} | {h:8.4f}")
    else:
        print(f"{nazwa:<25} | {'(brak pliku)':<24} | {'-':>8}")