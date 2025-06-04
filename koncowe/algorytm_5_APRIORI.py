from itertools import combinations, chain

transakcje = [
    ['kapusta', 'ogórki', 'pomidory', 'kabaczki'],
    ['ogórki', 'pomidory', 'kabaczki'],
    ['cytryny', 'pomidory', 'woda'],
    ['cytryny', 'woda', 'jajka'],
    ['ogórki', 'grzybki', 'żołądkowa'],
    ['żołądkowa', 'ogórki', 'pomidory'],
]

transakcje = list(map(set, transakcje))

def apriori(transakcje, min_support):

    jedynki = sorted(set(chain(*transakcje)))
    Fk = {frozenset([item]) for item in jedynki}
    F1 = {f for f in Fk if sum(f.issubset(t) for t in transakcje) >= min_support}

    wszystkie_F = []
    k = 1
    while F1:
        wszystkie_F.append(F1)

        kandydaci = set()
        for a, b in combinations(F1, 2):
            unia = a | b
            if len(unia) == k + 1 and all(
                frozenset(sub) in F1 for sub in combinations(unia, k)
            ):
                kandydaci.add(unia)

        Fk_plus_1 = {
            c for c in kandydaci
            if sum(c.issubset(t) for t in transakcje) >= min_support
        }

        F1 = Fk_plus_1
        k += 1

    return wszystkie_F

def generuj_reguly(wszystkie_F, transakcje, progi):
    liczba_transakcji = len(transakcje)
    reguly_na_prog = {p: [] for p in progi}

    support_map = {}
    for poziom in wszystkie_F:
        for zbior in poziom:
            support_map[zbior] = sum(zbior.issubset(t) for t in transakcje)

    for poziom in wszystkie_F[1:]:
        for zbior in poziom:
            sup_zbior = support_map[zbior] / liczba_transakcji
            for i in range(1, len(zbior)):
                for antecedent in combinations(zbior, i):
                    antecedent = frozenset(antecedent)
                    consequent = zbior - antecedent
                    sup_ant = support_map[antecedent]
                    confidence = support_map[zbior] / sup_ant
                    jakosc = sup_zbior * confidence

                    for p in progi:
                        if jakosc >= p:
                            reguly_na_prog[p].append(
                                (antecedent, consequent, sup_zbior, confidence, jakosc)
                            )
    return reguly_na_prog

MIN_SUPPORT = 2
PROGI_JAKOSCI = [0.1, 0.2, 0.3, 0.4]
czeste_zbiory = apriori(transakcje, MIN_SUPPORT)

print("Częste zbiory:")
for poziom, Fi in enumerate(czeste_zbiory, 1):
    print(f"F{poziom}: {Fi}")

reguly = generuj_reguly(czeste_zbiory, transakcje, PROGI_JAKOSCI)

print("\nReguły asocjacyjne według progów jakości (support × confidence):")
for prog in sorted(PROGI_JAKOSCI):
    print(f"\n≥ {prog:.1f}")
    for ant, cons, sup, conf, jakosc in reguly[prog]:
        print(
            f"{set(ant)} → {set(cons)}  "
            f"sup={sup:.2f}, conf={conf:.2f}, sup×conf={jakosc:.2f}"
        )
