# Raport Laboratorium 7 SQL Injection i Code Injection

## Zadanie 1 SQL Injection

W pliku aplikacja/app.py w funkcji sekret() zmienna klucz jest doklejana bezposrednio do zapytania SQL przez +. Jak wpisalem sam apostrof ', dostalem 0 wierszy i blad OperationalError: unrecognized token: "'''", bo moj apostrof zamknal napis w zapytaniu za wczesnie i na koncu zostal 1 niedomkniety apostrof

Przetestowalem 5 wejsc i otrzymalem nastepujaca liczbe wierszy:
- 1234: 1 wiersz (anna: Hello world)
- ': 0 wierszy (blad skladni SQLite)
- ' OR '1'='1: 4 wiersze (wszystkie sekrety z tabeli sekrety)
- ' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --: 2 wiersze (schematy tabel)
- ' UNION SELECT login, rola || ' - ' || email FROM konta --: 2 wiersze (dane uzytkownikow z tabeli konta)

Zapytanie po wstawieniu danych dla ataku na sqlite_master:
SELECT wlasciciel, sekret FROM sekrety WHERE klucz = '' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --'


W bazie zidentyfikowalem dwie tabele: konta oraz sekrety, a w drugiej tabeli (konta) odczytalem kolumny: login, rola, email

Wyjasnienie zmiany struktury zapytania:
moj apostrof zamknal napis w WHERE, przez co wszystko co wpisalem dalej baza potraktowala jako normalny kod SQL (np OR czy UNION SELECT), a -- zakomentowalo reszte oryginalnego zapytania

## Zadanie 2 Zapytanie z parametrami

Zamiast sklejac napisy dalem zapytanie z parametrem ? i krotka (klucz,), a szczegoly bledu przerzucilem do logow przez app.logger.exception(...):
zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
wiersze = db.execute(zapytanie, (klucz,)).fetchall()


Po restarcie kontenera powtorzylem 5 wejsc z zadania 1 oraz klucz d'Artagnan i porownalem liczbe zwroconych wierszy:

| Wejscie (klucz) | Przed poprawka | Po poprawce |
| :--- | :---: | :---: |
| 1234 | 1 | 1 |
| ' | 0 (blad SQLite) | 0 |
| ' OR '1'='1 | 4 | 0 |
| ' UNION SELECT name, sql FROM sqlite_master WHERE type='table' -- | 2 | 0 |
| ' UNION SELECT login, rola \|\| ' - ' \|\| email FROM konta -- | 2 | 0 |
| d'Artagnan | 0 (blad SQLite) | 1 |

W logach serwera i na stronie po poprawce nie otrzymalem zadnych komunikatow bledow SQLite ani danych z nieuprawnionych zapytan

Wyjasnienie dzialania parametrow:
baza najpierw przygotowuje strukture zapytania, a dopiero potem podstawia wartosc z krotki, wiec traktuje ja tylko jako zwykly tekst, a nie kod SQL; Parametr ? dziala tylko dla wartosci i nie da sie nim zastapic nazwy tabeli ani kolumny

## Zadanie 3 Code Injection w kalkulatorze

W aplikacja/app.py w funkcji kalkulator() znalazlem wywolanie eval(wyrazenie) i przed zmiana kodu wykonalem 3 ataki:
- __import__('os').listdir('/etc') -> otrzymalem liste 46 plikow i katalogow w /etc (m.in. alpine-release, os-release, passwd, shadow)
- open('/etc/os-release').read() -> odczytalem nazwe i wersje systemu: NAME="Alpine Linux", VERSION_ID=3.24.4 (PRETTY_NAME="Alpine Linux v3.24")
- __import__('os').getuid() -> odczytalem UID procesu aplikacji: 1000 (uzytkownik app)

Zastapilem eval wlasnym parserem sprawdzajacym limit 100 znakow, dopasowanie calego napisu przez re.fullmatch do formatu liczba operator liczba oraz slownik dozwolonych operacji (+, -, *, /), a po restarcie wykonalem 8 testow:

| Test (wyrazenie) | Kod HTTP | Wynik po poprawce |
| :--- | :---: | :--- |
| 2+3 | 200 | 5.0 |
| 7 / 2 | 200 | 3.5 |
| -1.5*4 | 200 | -6.0 |
| 1/0 | 400 | blad: dzielenie przez zero |
| __import__('os').listdir('/etc') | 400 | blad: nieprawidlowe wyrazenie |
| open('/etc/os-release').read() | 400 | blad: nieprawidlowe wyrazenie |
| __import__('os').getuid() | 400 | blad: nieprawidlowe wyrazenie |
| (puste pole ?wyrazenie=) | 400 | blad: nieprawidlowe wyrazenie |

Wyjasnienie przewagi bialej listy:
blokowanie pojedynczych slow jak import nic nie daje, bo dalej mozna odpalic inne wbudowane funkcje w Pythonie (np open) albo obejsc filtr na inne sposoby, a biala lista przepuszcza tylko dokladny format dzialania i odrzuca cala reszte