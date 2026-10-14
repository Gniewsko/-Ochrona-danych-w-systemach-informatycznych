import math
import os


def oblicz_entropie_pliku(sciezka: str) -> float:
    # 1. Odczyt surowych bajtow z pliku
    with open(sciezka, "rb") as f:
        dane = f.read()

    if not dane:
        return 0.0

    # 2. Histogram wystapien bajtow
    stat = {}
    for b in dane:
        stat[b] = stat.get(b, 0) + 1

    # 3. Suma Shannona
    n = len(dane)
    entropia = 0.0
    for ilosc in stat.values():
        p = ilosc / n
        entropia -= p * math.log2(p)

    return entropia, n


def main():
    nazwa_pliku = input("Podaj nazwe pliku (np. crypto.rot lub crypto.rc4): ").strip()

    if not os.path.exists(nazwa_pliku):
        print(f"Blad: plik '{nazwa_pliku}' nie istnieje w biezacym katalogu.")
        return

    h, rozmiar = oblicz_entropie_pliku(nazwa_pliku)

    print(f"\nPlik:     {nazwa_pliku}")
    print(f"Rozmiar:  {rozmiar} bajtow")
    print(f"Entropia: {h:.4f} bitow/bajt")


if __name__ == "__main__":
    main()