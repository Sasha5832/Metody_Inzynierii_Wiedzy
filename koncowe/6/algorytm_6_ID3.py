import csv
import math
from collections import Counter, defaultdict
from pathlib import Path


def entropia(przyklady, decyzyjny):
    suma = len(przyklady)
    zliczenia = Counter(r[decyzyjny] for r in przyklady)
    return -sum((c / suma) * math.log2(c / suma) for c in zliczenia.values())


def podziel(przyklady, atrybut):
    czesci = defaultdict(list)
    for wiersz in przyklady:
        czesci[wiersz[atrybut]].append(wiersz)
    return czesci


def zysk(przyklady, atrybut, decyzyjny):
    rodzic = entropia(przyklady, decyzyjny)
    suma = len(przyklady)
    wazona = sum(
        (len(p) / suma) * entropia(p, decyzyjny)
        for p in podziel(przyklady, atrybut).values()
    )
    return rodzic - wazona


def przewaga(przyklady, decyzyjny):
    return Counter(r[decyzyjny] for r in przyklady).most_common(1)[0][0]


class Wezel:
    def __init__(self, *, atrybut=None, etykieta=None):
        self.atrybut = atrybut
        self.etykieta = etykieta
        self.galezie = {}

    def wypisz(self, wciecie=""):
        if self.etykieta is not None:
            return wciecie + f"[klasa: {self.etykieta}]"
        linie = []
        for wartosc, pod in self.galezie.items():
            linie.append(wciecie + f"{self.atrybut} = {wartosc}:")
            linie.append(pod.wypisz(wciecie + "  "))
        return "\n".join(linie)


def id3(przyklady, atrybuty, decyzyjny):
    pierwsza = przyklady[0][decyzyjny]
    if all(r[decyzyjny] == pierwsza for r in przyklady):
        return Wezel(etykieta=pierwsza)
    if not atrybuty:
        return Wezel(etykieta=przewaga(przyklady, decyzyjny))

    najlepszy = max(atrybuty, key=lambda a: zysk(przyklady, a, decyzyjny))
    wezel = Wezel(atrybut=najlepszy)

    pozostale = [a for a in atrybuty if a != najlepszy]
    for wartosc, podzbior in podziel(przyklady, najlepszy).items():
        wezel.galezie[wartosc] = id3(podzbior, pozostale, decyzyjny)
    return wezel


def rozpoznaj(sciezka: Path):
    probka = sciezka.open(encoding="utf-8").read(4096)
    try:
        return csv.Sniffer().sniff(probka)
    except csv.Error:
        class Tab(csv.excel):
            delimiter = "\t"
        return Tab


def wczytaj(sciezka: Path):
    dialekt = rozpoznaj(sciezka)
    wiersze = list(csv.reader(sciezka.open(encoding="utf-8"), dialekt))
    if not wiersze:
        raise ValueError("Pusty plik!")
    naglowki = wiersze[0]
    decyzyjny = naglowki[-1]
    przyklady = [dict(zip(naglowki, w)) for w in wiersze[1:]]
    atrybuty = naglowki[:-1]
    return przyklady, atrybuty, decyzyjny


def main():
    plik = Path(__file__).with_name("SystemDecyzyjny.txt")
    if not plik.exists():
        raise FileNotFoundError(f"Brak pliku {plik}")
    przyklady, atrybuty, decyzyjny = wczytaj(plik)
    drzewo = id3(przyklady, atrybuty, decyzyjny)
    print("\nWygenerowane drzewo decyzyjne:")
    print(drzewo.wypisz())


if __name__ == "__main__":
    main()
