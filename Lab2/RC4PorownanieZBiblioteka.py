try:
    from Crypto.Cipher import ARC4
except ImportError:
    from Cryptodome.Cipher import ARC4

# Poluzowanie wymogu minimalnej dlugosci klucza (zgodnie ze wskazowka z ISOD)
ARC4.key_size = range(1, 257)


# 1. Własna implementacja RC4
def wlasny_rc4(dane: bytes, klucz: bytes) -> bytes:
    # Inicjalizacja tablicy S (KSA)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + klucz[i % len(klucz)]) % 256
        S[i], S[j] = S[j], S[i]

    # PRGA + XOR
    i = 0
    j = 0
    wynik = bytearray()
    for bajt in dane:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        wynik.append(bajt ^ K)

    return bytes(wynik)


# 2. Porównanie obu implementacji
def main():
    print("=== TEST ZGODNOŚCI Z PYCRYPTODOME (ARC4) ===")

    tekst = input("Podaj wiadomosc: ").encode("utf-8")
    klucz = input("Podaj klucz: ").encode("utf-8")

    # Szyfrowanie wlasnym algorytmem
    wynik_wlasny = wlasny_rc4(tekst, klucz)

    # Szyfrowanie biblioteka PyCrypto / PyCryptodome
    cipher = ARC4.new(klucz)
    wynik_biblioteka = cipher.encrypt(tekst)

    print("\n--- WYNIKI ---")
    print(f"Własna funkcja (hex):  {wynik_wlasny.hex()}")
    print(f"Biblioteka ARC4 (hex): {wynik_biblioteka.hex()}")

    # Asercja sprawdzająca zgodność
    if wynik_wlasny == wynik_biblioteka:
        print("\nZgodność potwierdzona: oba wyniki są identyczne.")
    else:
        print("\nBŁĄD: wyniki się różnią!")


if __name__ == "__main__":
    main()