# Raport Laboratorium 8 RSA i podpis cyfrowy

## Zadanie 1 RSA na małych liczbach

W zadaniu 1 napisałem własną funkcję szybkiego potęgowania modularnego oraz rozkładu liczby n na czynniki pierwsze metodą dzielenia próbnego. Po uruchomieniu programu otrzymałem wynik:

p=1048601, q=1398107, d=1396416556673, czas=171.5071 ms
Tekst: Klucz RSA o długości 41 bitów rozkładasz na czynniki w ułamku sekundy. Bezpieczne RSA ma co najmniej 2048 bitów.

Odczytane wartości to p = 1048601, q = 1398107 oraz klucz prywatny d = 1396416556673, a czas faktoryzacji wyniósł 171.5071 ms.

Dlaczego ta metoda nie złamie klucza 2048 bitów:
Dzielenie próbne musi sprawdzać potencjalne dzielniki aż do pierwiastka z liczby n, co dla klucza 2048-bitowego oznacza około 2^1024 możliwości i zajęłoby niewyobrażalnie dużo czasu, dlatego w praktyce jest niemożliwe do wykonania

## Zadanie 2 Podpisy RSA-PSS

W zadaniu 2 zweryfikowałem podpisy czterech dokumentów przy użyciu klucza publicznego klucz_podpisu.pem, wygenerowałem własną parę kluczy RSA o długości 3072 bitów, podpisałem plik podpis.txt i sprawdziłem działanie weryfikacji po zmianie jednego bajtu w pliku, otrzymałem wynik:

faktura.txt BŁĄD
protokol.txt OK
regulamin.txt BŁĄD
umowa.txt OK
wlasny podpis (przed): OK
wlasny podpis (po zmianie 1 B): BLAD

Weryfikacja dokumentów wyszła poprawnie (OK) dla plików protokol.txt i umowa.txt oraz błędna (BŁĄD) dla plików faktura.txt i regulamin.txt, natomiast mój własny podpis przeszedł weryfikację przed zmianą pliku (OK) i został odrzucony po zmianie jednego bajtu (BLAD)

Czego nie potwierdza poprawny podpis z niezaufanego klucza:
Poprawny podpis potwierdza tylko to, że plik nie został zmieniony i pasuje do danego klucza, ale jeśli klucz publiczny pochodzi z niezaufanego źródła, to nie mam żadnej pewności, kto naprawdę jest jego właścicielem i czy nie podstawił go ktoś inny

## Zadanie 3 Szyfrowanie hybrydowe

W zadaniu 3 sprawdziłem poprawność formatu pliku paczka.bin, odszyfrowałem go kluczem prywatnym z hasłem, przetestowałem odrzucenie pliku po zmianie jednego bajtu oraz utworzyłem zaszyfrowany plik odpowiedz.bin dla prowadzącego. Po uruchomieniu otrzymałem wynik:

L paczka.bin: 256
Gratulacje, paczka odszyfrowana poprawnie.
[...]
Klucz AES tej wiadomości był losowy i zabezpieczony tylko algorytmem RSA-OAEP.

Zmiana 1 B: InvalidTag
L odpowiedz.bin: 384

Wartość L wyniosła 256 B dla pliku paczka.bin oraz 384 B dla pliku odpowiedz.bin, pierwszy wiersz odszyfrowanego tekstu to "Gratulacje, paczka odszyfrowana poprawnie.", a zmiana jednego bajtu w kryptogramie spowodowała odrzucenie pliku błędem InvalidTag bez zwrócenia tekstu

Dlaczego plik szyfrujemy AES, a RSA tylko klucz:
Szyfrowanie AES jest bardzo szybkie i nie ma ograniczenia rozmiaru danych, podczas gdy algorytm RSA-OAEP jest wolny i pozwala zaszyfrować naraz tylko bardzo krótką wiadomość (np. 190 B dla klucza 2048 bitów), więc używamy go tylko do bezpiecznego przesłania krótkiego klucza AES