import pandas as pd


data = {
    'obiekt': ['o1', 'o2', 'o3', 'o4', 'o5', 'o6', 'o7', 'o8'],
    'a1': [1, 1, 1, 1, 1, 1, 1, 1],
    'a2': [1, 1, 1, 1, 1, 1, 1, 1],
    'a3': [1, 1, 1, 1, 2, 2, 2, 2],
    'a4': [1, 1, 3, 3, 1, 1, 2, 2],
    'a5': [3, 3, 2, 3, 2, 2, 3, 4],
    'a6': [1, 2, 1, 2, 1, 2, 1, 1],
    'd': [1, 1, 0, 1, 0, 1, 0, 1]
}
df = pd.DataFrame(data)
df.set_index('obiekt', inplace=True)
print("Tabela decyzyjna:\n", df, "\n")


def covers(df, conditions):
    covered_objects = set(df.index)
    for attr, val in conditions.items():
        covered_objects = covered_objects.intersection(df.index[df[attr] == val])
    return covered_objects


def find_rule_covering(df, target_class, seed_object):
    conditions = {}
    other_class_objects = set(df.index[df['d'] != target_class])
    current_rule_covered = set(df.index)
    while len(current_rule_covered.intersection(other_class_objects)) > 0:
        best_attr = None
        best_val = None
        best_new_covered = None
        best_reduction = -1
        for attr in df.columns:
            if attr == 'd':
                continue

            seed_val = df.loc[seed_object, attr]
            if attr in conditions and conditions[attr] != seed_val:
                continue

            tentative_conditions = dict(conditions)
            tentative_conditions[attr] = seed_val
            new_covered = covers(df, tentative_conditions)
            old_bad = current_rule_covered.intersection(other_class_objects)
            new_bad = new_covered.intersection(other_class_objects)
            reduction = len(old_bad) - len(new_bad)

            if reduction > best_reduction:
                best_reduction = reduction
                best_attr = attr
                best_val = seed_val
                best_new_covered = new_covered

        conditions[best_attr] = best_val
        current_rule_covered = best_new_covered

    covered_same_class = set(o for o in current_rule_covered if df.loc[o, 'd'] == target_class)
    return conditions, covered_same_class


def induce_rules_for_class(df, target_class):
    to_cover = set(df.index[df['d'] == target_class])
    rules = []

    while len(to_cover) > 0:
        seed = next(iter(to_cover))
        conds, covered = find_rule_covering(df, target_class, seed)
        rules.append(conds)
        to_cover = to_cover - covered
    return rules


all_decisions = df['d'].unique()
all_rules = {}

for dec in all_decisions:
    rules_for_dec = induce_rules_for_class(df, dec)
    all_rules[dec] = rules_for_dec

print("Wygenerowane reguły decyzyjne:\n")
for dec_class, rules_list in all_rules.items():
    print(f"--- Decyzja d = {dec_class} ---")
    for i, cond in enumerate(rules_list, start=1):
        cond_str = " i ".join([f"({k}={v})" for k, v in cond.items()])
        print(f"Reguła {i}: jeśli {cond_str} to d={dec_class}")
    print()
