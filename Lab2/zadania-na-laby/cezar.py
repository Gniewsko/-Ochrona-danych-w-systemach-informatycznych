import sys

if len(sys.argv) < 2:
    sys.exit(1)

with open(sys.argv[1], "rb") as f:
    ctext = f.read()

kandydaci = []
for k in range(256):
    pt = bytes((b - k) % 256 for b in ctext)
    score = sum(1 for b in pt if (32 <= b <= 126) or b in (9, 10, 13)) / len(pt)
    kandydaci.append((score, k, pt))

kandydaci.sort(key=lambda item: (-item[0], item[1]))

print("TOP 5")
for score, k, pt in kandydaci[:5]:
    poczatek = repr(pt[:45].decode("latin-1", errors="replace"))
    print(f"k = {k} | udział: {score}% | początek: {poczatek}")

wybrany_k = int(input("\nWybierz k: "))
odkodowany = bytes((b - wybrany_k) % 256 for b in ctext)

with open("cezar.txt", "wb") as f:
    f.write(odkodowany)

print("Zapisano do cezar.txt")