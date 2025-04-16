import pandas as pd
from itertools import combinations
from collections import defaultdict

# TO ALGORYTM 1


data_list = [
    [1, 1, 1, 1, 3, 1, 1],
    [1, 1, 1, 1, 3, 2, 1],
    [1, 1, 1, 3, 2, 1, 0],
    [1, 1, 1, 3, 3, 2, 1],
    [1, 1, 2, 1, 2, 1, 0],
    [1, 1, 2, 1, 2, 2, 1],
    [1, 1, 2, 2, 3, 1, 0],
    [1, 1, 2, 2, 4, 1, 1]
]

data = pd.DataFrame(data_list, columns=['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'd'])


def indist_matrix(df, decision):
    matrix = {}
    for i in df.index:
        for j in df.index:
            if i < j and df.at[i, decision] != df.at[j, decision]:
                common_attrs = [col for col in df.columns if col != decision and df.at[i, col] == df.at[j, col]]
                matrix[(i, j)] = set(common_attrs)
    return matrix


matrix = indist_matrix(data, 'd')


def find_rules(df, matrix, decision):
    attrs = [col for col in df.columns if col != decision]
    unused_attrs = defaultdict(set)
    rules = defaultdict(list)

    for obj in df.index:
        obj_dec = df.at[obj, decision]
        found = False
        for r in range(1, len(attrs)+1):
            if found:
                break
            for comb in combinations(attrs, r):
                is_valid = True
                for (i, j), common in matrix.items():
                    if obj in (i,j) and set(comb).issubset(common):
                        is_valid = False
                        break
                if is_valid:
                    rule = (comb, tuple(df.loc[obj, list(comb)]), obj_dec)
                    rules[r].append(rule)
                    found = True
                    break

    final_rules = defaultdict(lambda: defaultdict(int))
    for order, rule_list in rules.items():
        for comb, vals, dec in rule_list:
            key = (comb, vals, dec)
            final_rules[order][key] += 1

    for order in sorted(final_rules):
        print(f"\nReguły rzędu {order}:")
        for (attrs, vals, dec), sup in final_rules[order].items():
            conditions = ' ∧ '.join(f'({attr} = {val})' for attr, val in zip(attrs, vals))
            if sup > 1:
                print(f"{conditions} ⇒ (d={dec})[{sup}]")
            else:
                print(f"{conditions} ⇒ (d={dec})")


find_rules(data, matrix, 'd')
