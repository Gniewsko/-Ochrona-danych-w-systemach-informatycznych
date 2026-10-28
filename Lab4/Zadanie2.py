import hashlib, hmac, os

baza = {}
for line in open('hasla.txt'):
    u, it, salt, h = line.strip().split(':')
    baza[u] = (int(it), bytes.fromhex(salt), h)

def weryfikuj(login, haslo):
    if login not in baza:
        return False
    it, salt, exp = baza[login]
    h = hashlib.pbkdf2_hmac('sha256', haslo.encode('utf-8'), salt, it, 32).hex()
    return hmac.compare_digest(h, exp)

print("anna, Kasztan-2026:", weryfikuj("anna", "Kasztan-2026"))
print("anna, kasztan-2026:", weryfikuj("anna", "kasztan-2026"))
print("piotr, Żółw na łące:", weryfikuj("piotr", "Żółw na łące"))
print("kasia, Kasztan-2026:", weryfikuj("kasia", "Kasztan-2026"))

def dodaj(login, haslo):
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac('sha256', haslo.encode('utf-8'), salt, 600000, 32).hex()
    baza[login] = (600000, salt, h)

dodaj("test1", "haslo123")
dodaj("test2", "haslo123")
print("rowne sole:", baza["test1"][1] == baza["test2"][1])
print("rowne skroty:", baza["test1"][2] == baza["test2"][2])
print("weryfikacja test1:", weryfikuj("test1", "haslo123"))
print("weryfikacja test2:", weryfikuj("test2", "haslo123"))