# Raport - Lab 4: Funkcje skrótu

### Zadanie 1 – Sumy kontrolne

uruchamianie: python3 Zadanie1.py

statusy plików:
dokumenty/budzet.csv: BŁĄD
dokumenty/dane.bin: OK
dokumenty/harmonogram.txt: BRAK
dokumenty/kontakt.txt: OK
dokumenty/regulamin.txt: OK
roznice bitow: 131 (na 256, zmiana jednej litery zmieniła ponad 51% bitów co potwierdza efekt lawinowy)
odp: zwykła suma kontrolna obok pliku nie zabezpiecza przed celowym atakiem bo ktoś podmieniający treść po prostu wyliczy i wklei nowy hash do pliku - żeby upewnić się co do źródła i integralności trzeba użyć HMACa ze wspólnym kluczem tajnym albo podpisu cyfrowego z kluczem publicznym

### Zadanie 2 – Przechowywanie haseł

uruchamianie: python3 Zadanie2.py

wyniki testów weryfikacji:
anna, Kasztan-2026: True
anna, kasztan-2026: False
piotr, Żółw na łące: True
kasia, Kasztan-2026: False
rowne sole: False
rowne skroty: False
weryfikacja test1: True
weryfikacja test2: True
oba konta logują się tym samym hasłem
odp: unikalna sól sprawia że identyczne hasła dają różne hashe i uniemożliwia korzystanie z gotowych rainbow tables a duża liczba iteracji celowo narzuca narzut czasowy dzięki czemu atak brute-force staje się zbyt wolny i nieopłacalny

### Zadanie 3 – Kolizje i paradoks urodzinowy

uruchamianie: python3 Zadanie3.py

para: v_org=7282, v_zm=1761, h24=aac6b9
liczba pasujacych do oryginalu v=0: 0
odp: z powodu paradoksu urodzinowego znalezienie jakiejkolwiek pary o identycznym skrócie wymaga tylko około O(2^(n/2)) prób (porównujemy 8192 * 8192 ~= 6,71 * 10^7 możliwych par na 16,8 mln wartości) natomiast trafienie w konkretny z góry narzucony skrót oryginału to złożoność O(2^n) więc szansa trafienia przy zaledwie 8192 wariantach wynosiła zaledwie ok. 0,05%