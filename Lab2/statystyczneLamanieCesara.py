# Odczyt pliku binarnego
with open("crypto.rot", "rb") as f:
    dane = f.read()

# Zliczanie wystapien bajtow do slownika
stat = {}
for b in dane:
    if b in stat:
        stat[b] += 1
    else:
        stat[b] = 1

# Znalezienie najczestszego bajtu
najczestszy_bajt = max(stat, key=stat.get)

# Hipoteza: najczestszy znak to litera 'e'
klucz = (najczestszy_bajt - ord("e")) % 256
print("Wykryty klucz:", klucz)

# Odszyfrowanie
tekst = bytes((b - klucz) % 256 for b in dane)

# Wyswietlenie poczatku tekstu
print(tekst[:250].decode("windows-1250", errors="ignore"))