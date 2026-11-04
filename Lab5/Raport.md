# Raport Laboratorium 5 Bezpieczenstwo serwera WWW

## Zadanie 1 Dostep do katalogow

Kody i zachowanie przed edycja konfiguracji:
- `/materialy/`: 200 OK (widoczna lista plikow w html)
- `/materialy/notatka.txt`: 200 OK (plik dostepny)
- `/wewnetrzne/`: 200 OK (widoczna lista plikow w html)
- `/wewnetrzne/plan.txt`: 200 OK (plik dostepny)

Kody i zachowanie po zmianie w dostep.conf i restarcie:
- `/materialy/`: 403 Forbidden (wylaczone listowanie przez Options -Indexes, brak pliku indeksu)
- `/materialy/notatka.txt`: 200 OK (bezposredni dostep do znanego pliku nadal dziala)
- `/wewnetrzne/`: 403 Forbidden (blokada calego katalogu)
- `/wewnetrzne/plan.txt`: 403 Forbidden (blokada Require all denied odcina tez pliki wewnatrz)

Wpis z logu serwera (odmowa dostepu):
```text
web-1 | [Wed Nov 04 11:36:57.037322 2026] [authz_core:error] [pid 9:tid 13] [client 172.18.0.1:34672] AH01630: client denied by server configuration: /usr/local/apache2/htdocs/wewnetrzne/
```

Wyjasnienie roznicy:
Wylaczenie listowania (Options -Indexes) uniemozliwia tylko generowanie spisu zawartosci przy braku pliku indeksu, pozostawiajac pliki o znanej nazwie dostepne, natomiast Require all denied calkowicie odcina dostep HTTP do calego katalogu i wszystkich plikow w srodku

Konsola i logi z zadania 1:
```text
PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/materialy/
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:18:09 GMT
Server: Apache
Content-Length: 305
Content-Type: text/html;charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Index of /materialy</title>
 </head>
 <body>
<h1>Index of /materialy</h1>
<ul><li><a href="/"> Parent Directory</a></li>
<li><a href="notatka.txt"> notatka.txt</a></li>
</ul>
</body></html>

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/materialy/notatka.txt
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:18:10 GMT
Server: Apache
Last-Modified: Wed, 04 Nov 2026 09:21:42 GMT
ETag: "45-65f6fe8341580"
Accept-Ranges: bytes
Content-Length: 69
Content-Type: text/plain; charset=UTF-8

Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem.

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/wewnetrzne/
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:18:10 GMT
Server: Apache
Content-Length: 301
Content-Type: text/html;charset=ISO-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
 <head>
  <title>Index of /wewnetrzne</title>
 </head>
 <body>
<h1>Index of /wewnetrzne</h1>
<ul><li><a href="/"> Parent Directory</a></li>
<li><a href="plan.txt"> plan.txt</a></li>
</ul>
</body></html>

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/wewnetrzne/plan.txt
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:18:12 GMT
Server: Apache
Last-Modified: Wed, 04 Nov 2026 09:21:42 GMT
ETag: "3a-65f6fe8341580"
Accept-Ranges: bytes
Content-Length: 58
Content-Type: text/plain; charset=UTF-8

Fikcyjny plan: ten katalog ma byc niedostepny przez HTTP.

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose restart web
[+] restart 0/1
 - Container pliki-dla-studentow-web-1 Restarting                                                                 1.6s

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/materialy/
HTTP/1.1 403 Forbidden
Date: Wed, 04 Nov 2026 11:36:56 GMT
Server: Apache
Content-Length: 239
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/materialy/notatka.txt
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:36:57 GMT
Server: Apache
Last-Modified: Wed, 04 Nov 2026 09:21:42 GMT
ETag: "45-65f6fe8341580"
Accept-Ranges: bytes
Content-Length: 69
Content-Type: text/plain; charset=UTF-8

Publiczna notatka: ten plik ma pozostac dostepny pod znanym adresem.

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/wewnetrzne/
HTTP/1.1 403 Forbidden
Date: Wed, 04 Nov 2026 11:36:57 GMT
Server: Apache
Content-Length: 239
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/wewnetrzne/plan.txt
HTTP/1.1 403 Forbidden
Date: Wed, 04 Nov 2026 11:36:58 GMT
Server: Apache
Content-Length: 239
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body></html>
```

## Zadanie 2 Katalog dostepny na haslo

Baze hasel z kontem student zalozylem w /auth/uzytkownicy narzedziem htpasswd z flaga -cB. W dostep.conf zabezpieczylem sciezke /panel mechanizmem Basic z AuthName "Laboratorium 5"

Wyniki testow:
- `/panel/raport.txt` bez logowania: 401 Unauthorized
- `/panel/raport.txt` ze zlym haslem: 401 Unauthorized
- `/panel/raport.txt` z poprawnym haslem: 200 OK
- `/` bez logowania: 200 OK (strona glowna pozostala publiczna)

Naglowek przy braku logowania:
```http
WWW-Authenticate: Basic realm="Laboratorium 5"
```

Wyjasnienie braku ochrony w HTTP:
Basic w czystym HTTP przesyla poswiadczenia w naglowku Authorization zakodowane jedynie w Base64 bez szyfrowania, przez co kazdy moze je przechwycic i odczytac w sieci, pelna ochrone transmisji zapewnia dopiero HTTPS

Konsola i logi z zadania 2:
```text
PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose run --rm --no-deps narzedzia -cB /auth/uzytkownicy student
Container pliki-dla-studentow-narzedzia-run-c5d4b074c32b Creating
Container pliki-dla-studentow-narzedzia-run-c5d4b074c32b Created
New password:
Re-type new password:
Adding password for user student

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose exec web httpd -t
Syntax OK

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose restart web
[+] restart 0/1
 - Container pliki-dla-studentow-web-1 Restarting                                                                1.6s

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 401 Unauthorized
Date: Wed, 04 Nov 2026 11:55:08 GMT
Server: Apache
WWW-Authenticate: Basic realm="Laboratorium 5"
Content-Length: 421
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
</body></html>

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i -u student:zlehaslo http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 401 Unauthorized
Date: Wed, 04 Nov 2026 11:55:34 GMT
Server: Apache
WWW-Authenticate: Basic realm="Laboratorium 5"
Content-Length: 421
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
</body></html>

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i -u student:2137 http://127.0.0.1:8080/panel/raport.txt
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:56:12 GMT
Server: Apache
Last-Modified: Wed, 04 Nov 2026 09:21:42 GMT
ETag: "3a-65f6fe8341580"
Accept-Ranges: bytes
Content-Length: 58
Content-Type: text/plain; charset=UTF-8

Raport cwiczeniowy: dostep po poprawnym uwierzytelnieniu.

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 11:57:05 GMT
Server: Apache
Last-Modified: Wed, 04 Nov 2026 09:21:42 GMT
ETag: "15f-65f6fe8341580"
Accept-Ranges: bytes
Content-Length: 351
Content-Type: text/html; charset=UTF-8

<!doctype html>
<html lang="pl"><meta charset="utf-8"><title>Laboratorium 5</title>
<h1>Laboratorium 5: serwer WWW działa</h1>
<p>Materiały ćwiczeniowe do konfiguracji dostępu w Apache.</p>
<ul><li><a href="/materialy/">Materiały</a></li>
<li><a href="/wewnetrzne/">Wewnętrzne</a></li>
<li><a href="/panel/raport.txt">Panel</a></li></ul></html>
```

## Zadanie 3 Uprawnienia programu CGI

Napisalem skrypt cgi-bin/uprawnienia.cgi w Pythonie 3 z naglowkiem Content-Type, koncem linii LF i obsluga wyjatkow przy probie odczytu plikow. Przebudowalem obraz przez docker compose up -d --build web

Tozsamosc procesu i prawa plikow:
- Skrypt CGI dziala jako UID: 2, GID: 2 (uzytkownik daemon)
- `/lab-data/ogolny.txt`: uprawnienia 640, wlasciciel UID 0 (root), grupa GID 2 (daemon)
- `/lab-data/poufny.txt`: uprawnienia 600, wlasciciel UID 0 (root), grupa GID 2 (daemon)

Wyniki prob odczytu:
- `ogolny.txt`: odczytany pomyslnie (proces ma GID 2, co odpowiada uprawnieniom grupy w prawach 640)
- `poufny.txt`: odmowa odczytu Permission denied (prawa 600 zezwalaja na dostep wylacznie wlascicielowi UID 0)

Kody HTTP dla CGI przed i po dodaniu Basic:
- Przed Basic: 200 OK
- Po wlaczeniu Basic bez hasla: 401 Unauthorized
- Po wlaczeniu Basic z haslem: 200 OK (UID: 2, GID: 2 i wyniki odczytow pozostaly bez zmian)

Wyjasnienie tozsamosci procesu:
Zalogowanie przez HTTP weryfikuje uzytkownika jedynie w warstwie aplikacji Apache (zmienna REMOTE_USER), nie zmieniajac systemowego UID/GID procesu CGI, ktory caly czas dziala z uprawnieniami nieuprzywilejowanego uzytkownika daemon

Konsola i logi z zadania 3:
```text
PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose up -d --build web
[+] Building 5.4s (14/14) FINISHED
[+] up 2/2
 ✔ Image ochrona-danych-lab05:local    Built                                                                     5.8s
 ✔ Container pliki-dla-studentow-web-1 Started                                                                   2.9s

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose exec web ls -ln /lab-data/
total 8
-rw-r-----    1 0        2               48 Nov  4 09:21 ogolny.txt
-rw-------    1 0        2               61 Nov  4 09:21 poufny.txt

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 12:18:40 GMT
Server: Apache
Transfer-Encoding: chunked
Content-Type: text/plain; charset=utf-8

UID: 2
GID: 2
ogolny.txt: LAB05: dokument dostepny dla grupy procesu WWW.
poufny.txt: BLAD ([Errno 13] Permission denied: '/lab-data/poufny.txt')

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose exec web httpd -t
Syntax OK

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> docker compose restart web
[+] restart 0/1
 - Container pliki-dla-studentow-web-1 Restarting                                                                1.6s

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 401 Unauthorized
Date: Wed, 04 Nov 2026 12:26:31 GMT
Server: Apache
WWW-Authenticate: Basic realm="Laboratorium 5"
Content-Length: 421
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
</body></html>

PS C:\Users\Gniewko\Desktop\Priad\tle\-Ochrona-danych-w-systemach-informatycznych\Lab5\pliki-dla-studentow> curl.exe -i -u student:2137 http://127.0.0.1:8080/cgi-bin/uprawnienia.cgi
HTTP/1.1 200 OK
Date: Wed, 04 Nov 2026 12:27:14 GMT
Server: Apache
Transfer-Encoding: chunked
Content-Type: text/plain; charset=utf-8

UID: 2
GID: 2
ogolny.txt: LAB05: dokument dostepny dla grupy procesu WWW.
poufny.txt: BLAD ([Errno 13] Permission denied: '/lab-data/poufny.txt')
```