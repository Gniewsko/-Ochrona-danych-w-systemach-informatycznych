from pathlib import Path
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

pss = padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=32)
pub = serialization.load_pem_public_key(Path("pliki-dla-studentow/klucz_podpisu.pem").read_bytes())

for nazwa in ["faktura.txt", "protokol.txt", "regulamin.txt", "umowa.txt"]:
    dane = Path(f"pliki-dla-studentow/dokumenty/{nazwa}").read_bytes()
    sig = Path(f"pliki-dla-studentow/dokumenty/{nazwa}.sig").read_bytes()
    try:
        pub.verify(sig, dane, pss, hashes.SHA256())
        print(nazwa, "OK")
    except InvalidSignature:
        print(nazwa, "BŁĄD")

priv = rsa.generate_private_key(65537, 3072)
Path("moj_klucz_prywatny.pem").write_bytes(
    priv.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
)
Path("moj_klucz_publiczny.pem").write_bytes(
    priv.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
)

msg = b"Laboratorium 8: Gniewko"
sig = priv.sign(msg, pss, hashes.SHA256())
Path("podpis.txt").write_bytes(msg)
Path("podpis.txt.sig").write_bytes(sig)

priv.public_key().verify(sig, msg, pss, hashes.SHA256())
print("wlasny podpis (przed):", "OK")

kopia = bytearray(msg)
kopia[0] ^= 1
try:
    priv.public_key().verify(sig, bytes(kopia), pss, hashes.SHA256())
except InvalidSignature:
    print("wlasny podpis (po zmianie 1 B):", "BLAD")