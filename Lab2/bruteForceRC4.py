import itertools
import math
import os
import time
import string


# 1. Prosta funkcja RC4 odszyfrowująca tylko fragment próbki
def rc4_fragment(dane_fragment: bytes, klucz: bytes) -> bytes:
    S = list(range(256))
    j = 0
    klucz_len = len(klucz)
    for i in range(256):
        j = (j + S[i] + klucz[i % klucz_len]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    wynik = bytearray()
    for bajt in dane_fragment:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        wynik.append(bajt ^ S[(S[i] + S[j]) % 256])
    return bytes(wynik)


# 2. Kryterium oceny kandydata (czy bajty to tekst czytelny)
def czy_tekst_czytelny(probka: bytes) -> bool:
    # Sprawdzamy czy co najmniej 90% znaków to drukowalne ASCII lub znaki białe
    czytelne = sum(1 for b in probka if 32 <= b <= 126 or b in (9, 10, 13))
    return (czytelne / len(probka)) >= 0.90


def main():
    print("=== ATAK BRUTE FORCE NA RC4 ===")

    nazwa_pliku = input(
        "Podaj nazwę pliku (np. crypto2.rc4 lub encrypted.3rc4): "
    ).strip()

    # Automatyczne szukanie w folderze skryptu
    katalog = os.path.dirname(os.path.abspath(__file__))
    sciezka = os.path.join(katalog, nazwa_pliku)

    if not os.path.exists(sciezka):
        print("Błąd: Plik nie istnieje.")
        return

    with open(sciezka, "rb") as f:
        kryptogram = f.read()

    dlugosc_klucza = int(
        input("Podaj przewidywaną długość klucza (np. 2 lub 3): ")
    )

    # Zbiór znaków do testowania (najczęściej małe/duże litery i cyfry)
    alfabet = (string.ascii_letters + string.digits).encode("ascii")
    liczba_kombinacji = len(alfabet) ** dlugosc_klucza

    print(f"\nPrzestrzeń kluczy do sprawdzenia: {liczba_kombinacji:,}")
    print("Rozpoczynanie ataku...")

    # Bierzemy próbkę pierwszych 40 bajtów do szybkiej weryfikacji
    probka = kryptogram[:40]

    start_czas = time.perf_counter()
    sprawdzone = 0
    znaleziony_klucz = None

    # itertools.product generuje wszystkie wariacje z powtórzeniami
    for krotka in itertools.product(alfabet, repeat=dlugosc_klucza):
        klucz_kandydat = bytes(krotka)
        sprawdzone += 1

        odszyfrowana_probka = rc4_fragment(probka, klucz_kandydat)

        if czy_tekst_czytelny(odszyfrowana_probka):
            znaleziony_klucz = klucz_kandydat
            break

    koniec_czas = time.perf_counter()
    czas_trwania = koniec_czas - start_czas
    predkosc = sprawdzone / max(czas_trwania, 0.0001)

    print("\n--- PODSUMOWANIE ATAKU ---")
    print(f"Czas trwania:      {czas_trwania:.3f} s")
    print(f"Sprawdzono kluczy: {sprawdzone} / {liczba_kombinacji}")
    print(f"Prędkość:          {predkosc:,.0f} kluczy/s")

    if znaleziony_klucz:
        print(
            f"\nSUKCES! Znaleziony klucz: {znaleziony_klucz} (tekst: {znaleziony_klucz.decode('latin-1')})"
        )

        # Odszyfrowanie pełnego pliku poprawnym kluczem
        pelny_tekst = rc4_fragment(kryptogram, znaleziony_klucz)
        print("\nPoczątek odszyfrowanego tekstu:")
        print(pelny_tekst[:250].decode("latin-1", errors="replace"))

        # Zapis do pliku
        plik_wyjsciowy = os.path.join(katalog, "odszyfrowane_bruteforce.txt")
        with open(plik_wyjsciowy, "wb") as f:
            f.write(pelny_tekst)
        print(f"\nZapisano pełny plik jako: {plik_wyjsciowy}")
    else:
        print("\nNie znaleziono klucza w wybranym alfabecie.")


if __name__ == "__main__":
    main()