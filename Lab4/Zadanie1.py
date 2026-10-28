import hashlib, os

def sha256_file(path):
    if not os.path.exists(path):
        return None
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

for line in open('SHA256SUMS.txt'):
    exp, path = line.strip().split('  ')
    act = sha256_file(path)
    status = "BRAK" if act is None else ("OK" if act == exp else "BŁĄD")
    print(f"{path}: {status}")

h1 = hashlib.sha256(b"Ala ma kota.").digest()
h2 = hashlib.sha256(b"Ola ma kota.").digest()
print("roznice bitow:", sum(bin(a ^ b).count('1') for a, b in zip(h1, h2)))