import pandas as pd
from itertools import combinations
from collections import defaultdict
from pathlib import Path


def macierz_nieodr(df, decyzyjny):
    m = {}
    for i in df.index:
        for j in df.index:
            if i < j and df.at[i, decyzyjny] != df.at[j, decyzyjny]:
                wsp = {
                    kol for kol in df.columns
                    if kol != decyzyjny and df.at[i, kol] == df.at[j, kol]
                }
                m[(i, j)] = wsp
    return m

def znajdz_reguly(df, macierz, decyzyjny):
    atrybuty = [c for c in df.columns if c != decyzyjny]
    tymczasowe = defaultdict(list)

    for ob in df.index:
        dec = df.at[ob, decyzyjny]
        for r in range(1, len(atrybuty) + 1):
            for komb in combinations(atrybuty, r):
                if all(
                    not (ob in (i, j) and set(komb).issubset(wsp))
                    for (i, j), wsp in macierz.items()
                ):
                    wart = tuple(df.loc[ob, list(komb)])
                    tymczasowe[r].append((komb, wart, dec))
                    break
            else:
                continue
            break

    reguly = defaultdict(lambda: defaultdict(int))
    for rzad, lista in tymczasowe.items():
        for komb, wart, dec in lista:
            reguly[rzad][(komb, wart, dec)] += 1

    for rzad in sorted(reguly):
        print(f"\nReguły rzędu {rzad}:")
        for (komb, wart, dec), sup in reguly[rzad].items():
            warunki = " ∧ ".join(f"({a} = {v})" for a, v in zip(komb, wart))
            if sup > 1:
                print(f"{warunki} ⇒ (d={dec})[{sup}]")
            else:
                print(f"{warunki} ⇒ (d={dec})")

plik = Path(__file__).with_name("SystemDecyzyjny.txt")
dane = pd.read_csv(plik, sep=r"\s+|,|\t", engine="python", header=None)
kolumny = [f"a{i}" for i in range(1, dane.shape[1])] + ["d"]
dane.columns = kolumny

mac = macierz_nieodr(dane, "d")
znajdz_reguly(dane, mac, "d")
