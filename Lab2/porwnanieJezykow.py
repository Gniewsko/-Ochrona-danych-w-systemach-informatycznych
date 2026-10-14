import math

# Przykładowe fragmenty tekstów w 3 językach
tekst_pl = """
Zadania tej gospodarki stypendialnej nie ograniczają się do pytania komu udzielić 
stypendium. Trzeba wiedzieć w jakiej formie czy pod jakimi warunkami je dać by nie 
poszło dla nauki na marne by rzeczywiście wpłynęło dodatnio na wydajność pracy.
"""

tekst_en = """
This is an open letter to Michael Moore regarding Bowling for Columbine. 
The film presents an argument about fear and violence in American society. 
Critics have pointed out that many statistics and scenes are misleading.
"""

tekst_de = """
Die Entwicklung der modernen Kryptographie begann mit der mathematischen 
Analyse historischer Chiffren. Die statistische Untersuchung von Buchstaben 
ermöglicht das Brechen einfacher Verschlüsselungsverfahren ohne Schlüssel.
"""


def zbadaj_tekst(tekst, nazwa_jezyka):
    # 1. Zliczanie tylko liter (zamienionych na male)
    stat = {}
    lacznie_liter = 0

    for znak in tekst.lower():
        if znak.isalpha():
            stat[znak] = stat.get(znak, 0) + 1
            lacznie_liter += 1

    # 2. Obliczenie entropii Shannona
    entropia = 0.0
    for ilosc in stat.values():
        p = ilosc / lacznie_liter
        entropia -= p * math.log2(p)

    # 3. Posortowanie liter od najczestszej do najrzadszej
    posortowane = sorted(stat.items(), key=lambda para: para[1], reverse=True)

    print(f"=== Język: {nazwa_jezyka} ===")
    print(f"Liczba liter: {lacznie_liter}")
    print(f"Entropia:     {entropia:.3f} bitów/litera")
    print("5 najczęstszych liter:")
    for litera, ilosc in posortowane[:5]:
        procent = (ilosc / lacznie_liter) * 100
        print(f"  '{litera}': {procent:5.2f}% ({ilosc} razy)")
    print()


# Porownanie
zbadaj_tekst(tekst_pl, "Polski")
zbadaj_tekst(tekst_en, "Angielski")
zbadaj_tekst(tekst_de, "Niemiecki")