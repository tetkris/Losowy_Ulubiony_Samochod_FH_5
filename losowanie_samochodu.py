import csv
import random
import os
import json

CSV_FILE = "samochody.csv"
STATE_FILE = "wylosowane_samochody.json"

def wczytaj_samochody(csv_file):
    samochody = []
    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
        for row in reader:
            samochody.append({
                "marka": row["marka"].strip('" '),
                "nazwa": row["nazwa"].strip('" '),
                "rocznik": row["rocznik"].strip('" ')
            })
    return samochody

def wczytaj_stan(state_file):
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def zapisz_stan(state_file, wylosowane):
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(list(wylosowane), f)

def losuj_samochod():
    samochody = wczytaj_samochody(CSV_FILE)
    wylosowane = wczytaj_stan(STATE_FILE)
    wszystkie = set(f"{s['marka']}|{s['nazwa']}|{s['rocznik']}" for s in samochody)
    niewylosowane = [s for s in samochody if f"{s['marka']}|{s['nazwa']}|{s['rocznik']}" not in wylosowane]

    if not niewylosowane:
        print("Wszystkie samochody zostały już wylosowane. Resetuję losowanie.")
        wylosowane = set()
        niewylosowane = samochody

    samochod = random.choice(niewylosowane)
    klucz = f"{samochod['marka']}|{samochod['nazwa']}|{samochod['rocznik']}"
    wylosowane.add(klucz)
    zapisz_stan(STATE_FILE, wylosowane)

    print(f"Wylosowany samochód: {samochod['marka']} {samochod['nazwa']} ({samochod['rocznik']})")

if __name__ == "__main__":
    losuj_samochod()
