from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

dane = b"0123456789ABCDEF" * 4
klucz = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
iv = get_random_bytes(16)

szyfr_ecb = AES.new(klucz, AES.MODE_ECB)
kryp_ecb = szyfr_ecb.encrypt(dane)

szyfr_cbc = AES.new(klucz, AES.MODE_CBC, iv)
kryp_cbc = szyfr_cbc.encrypt(dane)

print("ECB bloki:")
becb = []
for i in range(0, 64, 16):
    blok = kryp_ecb[i:i+16]
    becb.append(blok)
    print(blok.hex())

print("CBC bloki:")
bcbc = []
for i in range(0, 64, 16):
    blok = kryp_cbc[i:i+16]
    bcbc.append(blok)
    print(blok.hex())

print("ECB czy wszystkie 4 bloki sa rowne:", becb[0] == becb[1] == becb[2] == becb[3])
print("CBC czy blok 1 i blok 2 sa rowne:", bcbc[0] == bcbc[1])

deszyfr_ecb = AES.new(klucz, AES.MODE_ECB)
odzyecb = deszyfr_ecb.decrypt(kryp_ecb)

deszyfr_cbc = AES.new(klucz, AES.MODE_CBC, iv)
odzycbc = deszyfr_cbc.decrypt(kryp_cbc)

print("ECB czy odzyskano wejscie:", odzyecb == dane)
print("CBC czy odzyskano wejscie:", odzycbc == dane)