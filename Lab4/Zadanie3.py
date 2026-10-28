import hashlib

oryg = open('oryginal.txt', 'rb').readlines()
zm = open('zmieniony.txt', 'rb').readlines()

def wariant(linie, v):
    return b''.join(l[:-1] + b' \n' if (v >> i) & 1 else l for i, l in enumerate(linie))

def h24(dane):
    return hashlib.sha256(dane).hexdigest()[:6]

slow = {h24(wariant(oryg, v)): v for v in range(8192)}

para = None
pas0 = 0
horg = h24(wariant(oryg, 0))

for v in range(8192):
    h = h24(wariant(zm, v))
    if para is None and h in slow:
        para = (slow[h], v, h)
    if h == horg:
        pas0 += 1

print(f"para: v_org={para[0]}, v_zm={para[1]}, h24={para[2]}")
print(f"liczba pasujacych do oryginalu v=0: {pas0}")