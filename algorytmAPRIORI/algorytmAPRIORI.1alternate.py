from itertools import combinations


def apriori(transactions, min_support):
    transaction_list = list(map(set, transactions))
    item_set = set(item for transaction in transactions for item in transaction)

    freq_sets = []
    candidate_set = [{item} for item in item_set]

    k = 1
    while candidate_set:
        frequent_set = []
        item_count = {}

        for candidate in candidate_set:
            count = sum(1 for trans in transaction_list if candidate.issubset(trans))
            if count >= min_support:
                frequent_set.append(candidate)
                item_count[frozenset(candidate)] = count

        if not frequent_set:
            break

        freq_sets.append((k, frequent_set, item_count))

        candidate_set = [
            set.union(*comb) for comb in combinations(frequent_set, 2)
            if len(set.union(*comb)) == k + 1
        ]

        candidate_set = list(map(set, set(frozenset(i) for i in candidate_set)))

        k += 1

    return freq_sets


def association_rules(freq_sets, transaction_count, min_confidence):
    rules = []
    for k, sets, support_dict in freq_sets:
        if k == 1:
            continue
        for item_set in sets:
            for i in range(1, len(item_set)):
                for antecedent in combinations(item_set, i):
                    antecedent = frozenset(antecedent)
                    consequent = item_set - antecedent
                    antecedent_support = next(support_dict_fs for k_fs, sets_fs, support_dict_fs in freq_sets if
                                              antecedent in support_dict_fs)[antecedent]
                    confidence = support_dict[frozenset(item_set)] / antecedent_support
                    support = support_dict[frozenset(item_set)] / transaction_count
                    if confidence >= min_confidence:
                        rules.append({
                            "antecedent": set(antecedent),
                            "consequent": set(consequent),
                            "confidence": confidence,
                            "support": support
                        })
    return rules


# Przykładowe dane
transactions = [
    {'kapusta', 'ogórki', 'pomidory', 'kabaczki'},
    {'ogórki', 'pomidory', 'kabaczki'},
    {'cytryny', 'pomidory', 'woda'},
    {'cytryny', 'woda', 'jajka'},
    {'ogórki', 'grzybki', 'żołądkowa'},
    {'żołądkowa', 'ogórki', 'pomidory'}
]

min_support = 2
min_confidence = 1 / 3

freq_sets = apriori(transactions, min_support)

print("Frequent sets:")
for k, sets, counts in freq_sets:
    print(f"F{k}: {[set(s) for s in sets]}")

rules = association_rules(freq_sets, len(transactions), min_confidence)

print("\nAssociation Rules:")
for rule in rules:
    print(
        f"{rule['antecedent']} => {rule['consequent']}, support: {rule['support']:.2f}, confidence: {rule['confidence']:.2f}")
