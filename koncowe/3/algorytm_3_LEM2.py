import re
import numpy as np
import pandas as pd
from collections import Counter


def wczytaj_plik(nazwa="SystemDecyzyjny.txt"):
    wiersze = []
    for linia in open(nazwa, encoding="utf-8"):
        linia = linia.strip()
        if not linia:
            continue
        pola = re.split(r"[,\s;]+", linia)
        wiersze.append([int(p.rstrip(".")) for p in pola])
    return np.array(wiersze)


def str_kolumny(macierz):
    return [f"a{i+1}" for i in range(macierz.shape[1] - 1)] + ["d"]


def na_napisy(macierz):
    return np.array([[str(x) for x in w] for w in macierz])


def lem2_brut(alfa: np.ndarray):
    kolumny = str_kolumny(alfa)
    kol_war = kolumny[:-1]

    df = pd.DataFrame(na_napisy(alfa), columns=kolumny)

    klasy = [int(w[-1]) for w in alfa]
    grupy_klas = []
    for k in klasy:
        for zb in grupy_klas:
            if k in zb:
                zb.append(k)
                break
        else:
            grupy_klas.append([k])

    wiersze_klas = []
    for zb in grupy_klas:
        wiersze_klas.append([alfa[i].tolist()
                             for i in range(len(df))
                             if int(df[kolumny[-1]].iloc[i]) in zb])

    kolumny_klas = []
    for grupa in wiersze_klas:
        tmp = [[] for _ in range(len(grupa[0]))]
        for w in grupa:
            for i, el in enumerate(w):
                tmp[i].append(el)
        kolumny_klas.append(tmp)

    kol_sprawdz = [list(map(int, c)) for c in alfa.T]

    wynik = []
    znacznik = False
    tnr = 0

    def rek(kol, podlista, wolne_wiersze, wolne_kolumny, nr):
        nonlocal znacznik
        for t in podlista[:-1]:
            kol += 1
            grupy, wskazniki = [], []
            for idx, val in enumerate(t):
                if idx in wolne_wiersze and kol in wolne_kolumny:
                    for g, w in zip(grupy, wskazniki):
                        if val in g:
                            g.append(val)
                            w.append(idx)
                            break
                    else:
                        grupy.append([val])
                        wskazniki.append([idx])

            if not grupy:
                continue

            for g, w in zip(grupy, wskazniki):
                if len(wolne_wiersze) <= 2 or (
                        len(g) == len(wolne_wiersze)//2 + 1):
                    wynik[nr].extend([kol, g[0]])
                    pozostale = list((Counter(kol_sprawdz[kol]) - Counter(t)).elements())
                    wolne_kolumny.remove(kol)

                    if g[0] in pozostale:
                        if wolne_kolumny:
                            res = rek(-1, podlista, w if len(wolne_wiersze) <= 2 else w,
                                      wolne_kolumny, nr)
                            return res
                        znacznik = True
                    return w if len(w) > 1 else w[0]

    for podlista in kolumny_klas:
        if not podlista:
            continue
        aktywne_wiersze = list(range(len(podlista[0])))
        aktywne_kolumny = list(range(len(kol_sprawdz) - 1))

        while aktywne_wiersze:
            wynik.append([])
            ret = rek(-1, podlista,
                      aktywne_wiersze,
                      aktywne_kolumny.copy(),
                      tnr)

            if znacznik:
                reg = ' ∧ '.join(f"(a{wynik[tnr][i]+1} = {wynik[tnr][i+1]})"
                                 for i in range(0, len(wynik[tnr]), 2))
                lancuch = ' ⇒ '.join(f"(d = {c})"
                                     for c in sorted(set(klasy)))
                sup = len(ret) if isinstance(ret, list) else 1
                print(f"{reg} ⇒ {lancuch}" + (f"[{sup}]" if sup > 1 else ""))
                for r in (ret if isinstance(ret, list) else [ret]):
                    aktywne_wiersze.remove(r)
                znacznik = False
            else:
                reg = ' ∧ '.join(f"(a{wynik[tnr][i]+1} = {wynik[tnr][i+1]})"
                                 for i in range(0, len(wynik[tnr]), 2))
                d_val = podlista[-1][0]
                sup = len(ret) if isinstance(ret, list) else 1
                print(f"{reg} ⇒ (d = {d_val})" + (f"[{sup}]" if sup > 1 else ""))
                for r in (ret if isinstance(ret, list) else [ret]):
                    aktywne_wiersze.remove(r)
            tnr += 1


if __name__ == "__main__":
    macierz = wczytaj_plik()
    lem2_brut(macierz)
