import pandas as pd


def find_covering_rules(df):
    rules = []  # Lista przechowująca reguły
    uncovered = set(df.index)  # Obiekty do pokrycia

    while uncovered:
        best_rule = None
        best_covered = set()


        for attr in df.columns[:-1]:
            for value in df[attr].unique():

                matching_objects = df[df[attr] == value]

                if matching_objects['d'].nunique() == 1:
                    decision = matching_objects['d'].iloc[0]
                    covered_objects = set(matching_objects.index) & uncovered

                    if len(covered_objects) > len(best_covered):
                        best_rule = (attr, value, decision)
                        best_covered = covered_objects

        if best_rule:
            attr, value, decision = best_rule
            rules.append(f"({attr} = {value}) ⇒ (d = {decision})")
            uncovered -= best_covered
        else:
            break
    return rules
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
df.set_index("obiekt", inplace=True)
rules = find_covering_rules(df)
for rule in rules:
    print(rule)
