import itertools


def wczytaj_system(nazwa="SystemDecyzyjny.txt"):
    wiersze = [w.strip() for w in open(nazwa, encoding="utf-8") if w.strip()]
    dane = []
    for w in wiersze:
        pierwsze = w.split()[0].lower().rstrip(".")
        if pierwsze.startswith(("a", "d")):
            continue
        if pierwsze.startswith("o"):
            w = " ".join(w.split()[1:])
        wiersz = []
        for tok in w.replace(",", " ").replace(";", " ").split():
            tok = tok.rstrip(".")
            try:
                wiersz.append(int(tok))
            except ValueError:
                try:
                    wiersz.append(float(tok))
                except ValueError:
                    wiersz.append(tok)
        dane.append(wiersz)
    return dane, len(dane[0]) - 1

def generuj_reguly(obiekty, n_attr):
    reguly = {}

    for i, ob in enumerate(obiekty):
        dec = ob[-1]
        roznice = [
            {a for a in range(n_attr) if ob[a] != inne[a]}
            for inne in obiekty if inne[-1] != dec
        ]
        if not roznice or any(not r for r in roznice):
            continue

        prawidlowe = []
        for r in range(1, n_attr + 1):
            for komb in itertools.combinations(range(n_attr), r):
                komb_set = set(komb)
                if all(not komb_set.isdisjoint(rz) for rz in roznice):
                    prawidlowe.append(komb_set)

        minimalne = [
            k for k in prawidlowe
            if not any(m != k and m.issubset(k) for m in prawidlowe)
        ]

        for zbior in minimalne:
            warunki = tuple(sorted((a, ob[a]) for a in zbior))
            reguly[(warunki, dec)] = None

    rzymskie = ["I", "II", "III", "IV", "V", "VI", "VII"]
    wedlug_dl = {}
    for warunki, dec in reguly:
        sup = sum(
            1 for o in obiekty
            if o[-1] == dec and all(o[a] == v for a, v in warunki)
        )
        tekst = " ∧ ".join(f"(a{a+1} = {v})" for a, v in warunki)
        tekst += f"  ⟹  (d = {dec})"
        if sup > 1:
            tekst += f"[{sup}]"
        dl = len(warunki)
        wedlug_dl.setdefault(dl, []).append(tekst)

    for dlugosc in sorted(wedlug_dl):
        naglowek = rzymskie[dlugosc - 1] if dlugosc <= len(rzymskie) else str(dlugosc)
        print(naglowek)
        for linia in wedlug_dl[dlugosc]:
            print("  " + linia)
        print()

if __name__ == "__main__":
    dane, n_attr = wczytaj_system()
    generuj_reguly(dane, n_attr)
