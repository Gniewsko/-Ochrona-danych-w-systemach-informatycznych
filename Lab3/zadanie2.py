from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

haslo = "TestHasło3315!"

def wykonaj_test(dane):
    sol = get_random_bytes(16)
    iv = get_random_bytes(16)
    klucz = PBKDF2(haslo.encode("utf-8"), sol, dkLen=32, count=200000, hmac_hash_module=SHA256)
    
    szyfr = AES.new(klucz, AES.MODE_CBC, iv)
    dane_pad = pad(dane, 16)
    kryp = szyfr.encrypt(dane_pad)
    
    deszyfr = AES.new(klucz, AES.MODE_CBC, iv)
    odzy_pad = deszyfr.decrypt(kryp)
    odzy = unpad(odzy_pad, 16)
    
    print("poprawnosc odzyskania:", odzy == dane)
    print("dlugosc kryptogramu:", len(kryp))
    return kryp

print("test puste dane")
wykonaj_test(b"")

print("test 16 bajtow ascii")
wykonaj_test(b"0123456789ABCDEF")

f = open("wiadomosc.txt", "rb")
dane_plik = f.read()
f.close()

print("test wiadomosc.txt")
kryp1 = wykonaj_test(dane_plik)

print("ponowne szyfrowanie wiadomosc.txt")
kryp2 = wykonaj_test(dane_plik)

print("czy kryptogramy sa identyczne:")
print(kryp1 == kryp2)