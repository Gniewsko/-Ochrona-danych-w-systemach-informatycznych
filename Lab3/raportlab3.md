# Raport - Lab 3 

## Zadanie 1 ECB i CBC

### 1. Wyniki z konsoli

ECB bloki:
a5ba2b6280d433bccfe6a0461cb88c4e
a5ba2b6280d433bccfe6a0461cb88c4e
a5ba2b6280d433bccfe6a0461cb88c4e
a5ba2b6280d433bccfe6a0461cb88c4e

CBC bloki:
d06034f1a14ef6932f9e7c85db6ccf2f
0cbb93025aed3e1c242432e0685a7240
251ec11ca77490c6a800aa36c4691145
4312f4d75d96fde395f1327eb6cbfbb8

ECB czy wszystkie 4 bloki sa rowne: True
CBC czy blok 1 i blok 2 sa rowne: False
ECB czy odzyskano wejscie: True
CBC czy odzyskano wejscie: True

### 2. Wyjaśnienie obserwacji
Po zaszyfrowaniu zauważyłem, że w trybie ECB wszystkie cztery bloki kryptogramu wyszły dokładnie takie same, ponieważ każdy 16 bajtowy blok wejścia szyfrowany jest całkowicie niezależnie tym samym kluczem. W trybie CBC z kolei każdy blok wyszedł zupełnie inny, bo przed zaszyfrowaniem łączy się go operacją XOR z poprzednim blokiem szyfrogramu (a pierwszy blok z wylosowanym przeze mnie IV), dzięki czemu powtarzający się wzorzec w danych zostaje ukryty. Po odszyfrowaniu obu kryptogramów w obu przypadkach odzyskałem bajt po bajcie oryginalne dane wejściowe

## Zadanie 2 Szyfrowanie z hasłem

### 1. Wyniki testów (AES-CBC + PKCS#7)
test puste dane
poprawnosc odzyskania: True
dlugosc kryptogramu: 16

test 16 bajtow ascii
poprawnosc odzyskania: True
dlugosc kryptogramu: 32

test wiadomosc.txt
poprawnosc odzyskania: True
dlugosc kryptogramu: 256

ponowne szyfrowanie wiadomosc.txt
poprawnosc odzyskania: True
dlugosc kryptogramu: 256
czy kryptogramy sa identyczne:
False

### 2. Różnica między solą a IV
Sól wykorzystałem w funkcji PBKDF2 do bezpiecznego wyprowadzenia klucza z hasła, żeby chronić je przed tęczowymi tablicami i atakami słownikowymi (dzięki soli to samo hasło da inny klucz). Z kolei wektor IV był mi potrzebny do samego trybu CBC, żeby rozpoczęcie szyfrowania nie było przewidywalne i żeby ten sam klucz nie dawał identycznego kryptogramu na początku danych

## Zadanie 3 Odzyskanie słabego klucza (slaby_ecb.bin)

### 1. Wyniki rankingu TOP 5 kandydatów
5 najlepszych kandydatow:
znak: m entropia H: 4.4536
znak: b entropia H: 7.9472
znak: x entropia H: 7.949
znak: o entropia H: 7.9493
znak: 2 entropia H: 7.9502
pierwszy wiersz tekstu: Record 000. The archive contains laboratory notes about symmetric encryption and careful handlingof binary files.

### 2. Uzasadnienie i pytania
* **Dlaczego jest tylko 36 kluczy?**  
  Sprawdzałem tylko 36 kombinacji, ponieważ z treści zadania wynikało, że klucz tworzy jeden znak powtórzony 16 razy, a mogłem wybierać wyłącznie spośród 26 małych liter oraz 10 cyfr (26 + 10 = 36)
* **Czemu ranking entropii może zawieść dla danych skompresowanych?**  
  Taki ranking może zawieść przy plikach skompresowanych, bo kompresja usuwa powtórzenia i ujednolica rozkład bajtów. Wtedy poprawny tekst ma sam z siebie bardzo wysoką entropię (bliską 8 bitów na bajt), przez co nie da się go łatwo odróżnić od losowego szumu, który powstaje przy próbie odszyfrowania złym kluczem