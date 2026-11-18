"""Sejf sekretow i kalkulator - celowo podatna aplikacja do laboratorium 7.

Uruchamiaj wylacznie lokalnie, w kontenerze z pakietu. Dane sa fikcyjne.
"""
import operator
import re
import sqlite3

from flask import Flask, render_template, request

app = Flask(__name__)
BAZA = "file:/dane/sekrety.db?mode=ro"
OPERATORY = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sekret")
def sekret():
    klucz = request.args.get("klucz", "")
    zapytanie = "SELECT wlasciciel, sekret FROM sekrety WHERE klucz = ?"
    wiersze, blad = [], None
    try:
        with sqlite3.connect(BAZA, uri=True) as db:
            wiersze = db.execute(zapytanie, (klucz,)).fetchall()
    except sqlite3.Error:
        app.logger.exception("blad zapytania SQLite w /sekret")
        blad = "wystapil blad podczas przetwarzania zadania"
    return render_template("sekret.html", klucz=klucz, zapytanie=zapytanie, wiersze=wiersze, blad=blad)


@app.route("/kalkulator")
def kalkulator():
    if "wyrazenie" not in request.args:
        return render_template("kalkulator.html", wyrazenie="", wynik=None)

    wyrazenie = request.args["wyrazenie"]
    if len(wyrazenie) > 100:
        return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik="blad: za dlugie wyrazenie"), 400

    m = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)\s*", wyrazenie)
    if not m:
        return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik="blad: nieprawidlowe wyrazenie"), 400

    a, op, b = float(m[1]), m[2], float(m[3])
    if op == "/" and b == 0:
        return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik="blad: dzielenie przez zero"), 400

    return render_template("kalkulator.html", wyrazenie=wyrazenie, wynik=OPERATORY[op](a, b))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)