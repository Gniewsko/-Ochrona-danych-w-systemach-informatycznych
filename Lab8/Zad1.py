import math
import time
from pathlib import Path


def pow_mod(a, b, n):
    w = 1
    a %= n
    while b > 0:
        if b % 2 == 1:
            w = (w * a) % n
        a = (a * a) % n
        b //= 2
    return w


def faktor(n):
    for d in range(2, math.isqrt(n) + 1):
        if n % d == 0:
            return d, n // d


assert pow_mod(4, 13, 497) == 445
assert pow_mod(7, 0, 497) == 1

linie = Path("pliki-dla-studentow/male_rsa.txt").read_text().splitlines()
n = int(linie[0].split("=")[1])
e = int(linie[1].split("=")[1])
bloki = [int(x) for x in linie[2].split("=")[1].split(",")]

t0 = time.perf_counter()
p, q = faktor(n)
czas = (time.perf_counter() - t0) * 1000

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
assert (e * d) % phi == 1

bajty = b"".join(pow_mod(c, d, n).to_bytes(4, "big") for c in bloki)
print(f"p={p}, q={q}, d={d}, czas={czas:.4f} ms")
print("Tekst:", bajty.decode("utf-8").rstrip(" "))