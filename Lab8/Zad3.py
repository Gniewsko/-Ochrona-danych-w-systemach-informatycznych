import os
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SLOWO = "SZAFIR-58"

oaep = padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)


def odszyfruj(dane, priv):
    assert len(dane) >= 2
    L = int.from_bytes(dane[:2], "big")
    assert L == priv.key_size // 8 and len(dane) >= L + 30
    klucz_aes = priv.decrypt(dane[2 : 2 + L], oaep)
    tekst = AESGCM(klucz_aes).decrypt(dane[2 + L : 2 + L + 12], dane[2 + L + 12 :], None)
    return L, tekst.decode("utf-8")


priv = serialization.load_pem_private_key(
    Path("pliki-dla-studentow/klucz_prywatny.pem").read_bytes(), b"Lab8-cwiczenie"
)
paczka = Path("pliki-dla-studentow/paczka.bin").read_bytes()

L_paczka, tekst = odszyfruj(paczka, priv)
print("L paczka.bin:", L_paczka)
print(tekst)

zla = bytearray(paczka)
zla[-1] ^= 1
try:
    odszyfruj(bytes(zla), priv)
except Exception as e:
    print("Zmiana 1 B:", type(e).__name__)

if SLOWO:
    pub = serialization.load_pem_public_key(Path("pliki-dla-studentow/klucz_prowadzacego.pem").read_bytes())
    aes_key, nonce = os.urandom(32), os.urandom(12)
    ct = AESGCM(aes_key).encrypt(nonce, f"{SLOWO}\nGniewsko".encode("utf-8"), None)
    enc_key = pub.encrypt(aes_key, oaep)
    Path("odpowiedz.bin").write_bytes(len(enc_key).to_bytes(2, "big") + enc_key + nonce + ct)
    print("L odpowiedz.bin:", len(enc_key))