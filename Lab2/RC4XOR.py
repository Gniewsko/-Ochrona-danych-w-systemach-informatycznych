# 1. Generator strumienia klucza (KSA + PRGA)
def generuj_strumien_rc4(klucz: bytes):
    # --- Inicjalizowanie rejestru S (KSA) ---
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + klucz[i % len(klucz)]) % 256
        S[i], S[j] = S[j], S[i]

    # --- Generowanie strumienia klucza K (PRGA) ---
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K


# 2. Szyfrowanie / Odszyfrowanie za pomocą XOR
def rc4_xor(dane: bytes, klucz: bytes) -> bytes:
    strumien = generuj_strumien_rc4(klucz)
    wynik = bytearray()

    for bajt in dane:
        k = next(strumien)  # Pobieramy kolejny bajt klucza ze strumienia
        wynik.append(bajt ^ k)  # Operacja XOR: M[i] ^ K[i]

    return bytes(wynik)


# --- Działanie programu z wprowadzaniem z palca ---
def main():
    print("=== SZYFR STRUMIENIOWY RC4 ===")

    tekst = input("Podaj wiadomosc do zaszyfrowania: ")
    klucz_tekst = input("Podaj klucz: ")

    # Zamiana tekstu na bajty (UTF-8)
    dane = tekst.encode("utf-8")
    klucz = klucz_tekst.encode("utf-8")

    # Szyfrowanie
    kryptogram = rc4_xor(dane, klucz)

    print("\n--- WYNIKI ---")
    print(f"Tekst jawny:         {tekst}")
    # Wynik po XOR to surowe bajty, wiec w terminalu najlepiej pokazac hex
    print(f"Kryptogram (hex):    {kryptogram.hex()}")

    # Odszyfrowanie (dokladnie ta sama operacja XOR z tym samym kluczem)
    odszyfrowane_bajty = rc4_xor(kryptogram, klucz)
    odszyfrowany_tekst = odszyfrowane_bajty.decode("utf-8")
    print(f"Odszyfrowany tekst:  {odszyfrowany_tekst}")


if __name__ == "__main__":
    main()