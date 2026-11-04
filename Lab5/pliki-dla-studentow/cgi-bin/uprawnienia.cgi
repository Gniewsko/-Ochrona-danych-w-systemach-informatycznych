#!/usr/bin/python3
import os

print("Content-Type: text/plain; charset=utf-8\n")

print(f"UID: {os.geteuid()}")
print(f"GID: {os.getegid()}")

try:
    with open("/lab-data/ogolny.txt", "r") as f:
        print("ogolny.txt: " + f.read().strip())
except Exception as e:
    print(f"ogolny.txt: BLAD ({e})")

try:
    with open("/lab-data/poufny.txt", "r") as f:
        print("poufny.txt: " + f.read().strip())
except Exception as e:
    print(f"poufny.txt: BLAD ({e})")