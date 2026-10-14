# Raport – Lab 2

## Zadanie 1 Cezar (cezar.bin)

### 1. Wyniki rankingu TOP 5
1. k = 230 | udział: 100.00% | początek: 'Wkh#Qljkw#Ihuu|\r\rWkh#qljkw#ihuu|#ohiw#wkh#kdu'
2. k = 233 | udział: 100.00% | początek: 'The Night Ferry\n\nThe night ferry left the har'
3. k = 228 | udział: 99.48%  | początek: 'Ymj%Snlmy%Kjww~\x0f\x0fYmj%snlmy%kjww~%qjky%ymj%mfw'
4. k = 229 | udział: 99.48%  | początek: 'Xli$Rmklx$Jivv}\x0e\x0eXli$rmklx$jivv}$pijx$xli$lev'
5. k = 231 | udział: 99.48%  | początek: 'Vjg"Pkijv"Hgtt{\x0c\x0cVjg"pkijv"hgtt{"nghv"vjg"jct'

* Wybrane przesunięcie: k = 233
* Plik wyjściowy: cezar.txt
zaczyna się od: The Night Ferry


### 2. Uzasadnienie i pytania
* Dlaczego k = 233, a nie 230?  
  W obu przypadkach program wyliczył 100% znaków drukowalnych, ale tylko przy 233 dostałem normalny tekst po angielsku. Przy k = 230 wszystko było przesunięte za daleko i zamiast spacji wyskoczyły #.
* Czemu entropia nie wykryje klucza?  
  Bo Cezar to zwykłe podstawienie 1:1. Jak w oryginale spacja występuje 200 razy, to po przesunięciu jakiś inny bajt też wystąpi równe 200 razy. Zmieniają się same kody znaków, ale ich ilości w pliku są identyczne. Entropia liczy tylko te ilości, więc dla każdego z 256 przesunięć da ten sam wynik.

## Zadanie 2 Vigenere (tekst_pl.txt)

### 1. Rezultaty testów
* Szyfrowanie tekst_pl.txt kluczem ZAMEK zapisałem do vigenere.bin. Sprawdziłem programem odszyfrowanie ze źródłem - bajt po bajcie jest identyczne (zgodnosc: ok).
* Puściłem też w kodzie asercje na pusty ciąg b"" i tablicę bajtów 0-255 - testy przeszły bez błędu.

### 2. Szyfrowanie ciągu BRAMABRAMABRAMA (3 bloki po 5 B)
* Klucz SZYFR (m = 5):  
  95ac9a9393 95ac9a9393 95ac9a9393
* Klucz KOD (m = 3):  
  8da1859890 869d90918c 91968c9c85

### 3. Wyjaśnienie powtarzalności bloków
Słowo BRAMA ma 5 liter i klucz SZYFR też ma długość 5. Przez to każda kolejna BRAMA trafia dokładnie na te same litery hasła, więc na wyjściu dostajemy trzy identyczne klocki hex. Od razu widać powtarzalność i długość klucza.  
Przy KOD długości to 3 i 5, więc kolejne słowa szyfrują się innymi literami (raz od K, raz od O itd) i bloki się nie powtarzają.

## Zadanie 3 RC4 (rc4.bin)

### 1. Wyniki ataku Brute Force
* Test dwukrotnego szyfrowania: zgodność potwierdzona (test ok).
* Próby: 17 576
* Czas przeszukiwania: 4.835 s
* Uzyskany klucz: tat
* Entropia kryptogramu (rc4.bin): 7.9271 bitów/bajt
* Entropia odszyfrowanego tekstu (rc4.txt): 4.3259 bitów/bajt
* Plik wyjściowy: rc4.txt
* Ponowne szyfrowanie tekstu kluczem tat: 100% zgodności z rc4.bin (ponowne szyfr ok).

### 2. Ranking TOP 5 kandydatów
1. tat - H = 4.3910
2. neg - H = 7.4304
3. mcn - H = 7.4512
4. oxo - H = 7.4536
5. tnx - H = 7.4592

### 3. Odpowiedzi na pytania
* Czemu ponowne szyfrowanie odtwarza plik nawet przy złym kluczu?  
  Bo XOR jest symetryczny. Jak nałożę ten sam ciąg dwa razy pod rząd, to matematycznie wracam do punktu wyjścia. To potwierdza tylko, że funkcja RC4 poprawnie liczy operacje, a nie że tekst ma jakikolwiek sens.
* Kiedy ranking entropii zawiedzie?  
  Na bardzo krótkich plikach (losowy zły klucz może przypadkiem dać powtarzający się ciąg bajtów o niskiej entropii) albo gdy szyfrujemy plik, który sam z siebie jest skompresowany, np zip. Taki plik już na wejściu ma entropię (ok. 8), więc poprawne odszyfrowanie nic nie obniży.