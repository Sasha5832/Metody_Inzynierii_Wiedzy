from itertools import combinations, chain

# przykładowe dane
transactions = [
    ['kapusta', 'ogórki', 'pomidory', 'kabaczki'],
    ['ogórki', 'pomidory', 'kabaczki'],
    ['cytryny', 'pomidory', 'woda'],
    ['cytryny', 'woda', 'jajka'],
    ['ogórki', 'grzybki', 'żołądkowa'],
    ['żołądkowa', 'ogórki', 'pomidory']
]

# Funkcja tworząca częste zbiory (Apriori)
def apriori(transactions, min_support):
    item_set = set(chain(*transactions))
    item_sets = [{frozenset([item]) for item in item_set}]

    frequent_sets = []

    k = 0
    while True:
        current_itemset = item_sets[k]
        frequent_current = set()
        item_counts = {}

        for transaction in transactions:
            for candidate in current_itemset:
                if candidate.issubset(transaction):
                    item_counts[candidate] = item_counts.get(candidate, 0) + 1

        for item, count in item_counts.items():
            if count >= min_support:
                frequent_current.add(item)

        if not frequent_current:
            break

        frequent_sets.append(frequent_current)

        next_candidates = set()
        for combo in combinations(frequent_current, 2):
            union_set = combo[0].union(combo[1])
            if len(union_set) == k + 2:
                next_candidates.add(union_set)

        item_sets.append(next_candidates)
        k += 1

    return frequent_sets

# Generowanie reguł asocjacyjnych
def generate_rules(frequent_sets, transactions, min_confidence):
    rules = []
    transaction_count = len(transactions)

    for k, frequent_set in enumerate(frequent_sets[1:], start=1):
        for item_set in frequent_set:
            subsets = list(chain(*[combinations(item_set, i) for i in range(1, len(item_set))]))
            for subset in subsets:
                antecedent = frozenset(subset)
                consequent = item_set.difference(antecedent)

                antecedent_count = sum(1 for trans in transactions if antecedent.issubset(trans))
                rule_count = sum(1 for trans in transactions if item_set.issubset(trans))

                confidence = rule_count / antecedent_count
                support = rule_count / transaction_count

                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, support, confidence))

    return rules

# Uruchamiamy przykład
min_support = 2
frequent_itemsets = apriori(transactions, min_support)
print("Częste zbiory:")
for level, itemsets in enumerate(frequent_itemsets, 1):
    print(f"Poziom {level}: {itemsets}")

min_confidence = 1/3
rules = generate_rules(frequent_itemsets, transactions, min_confidence)
print("\nReguły asocjacyjne:")
for antecedent, consequent, support, confidence in rules:
    print(f"{set(antecedent)} => {set(consequent)}, support={support:.2f}, confidence={confidence:.2f}, support * confidence={support * confidence:.2f}")
