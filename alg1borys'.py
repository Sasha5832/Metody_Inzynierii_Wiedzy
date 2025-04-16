import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter

import re

def convert_to_strings(array):
    return np.array([[str(val) for val in row] for row in array])

array = np.array([
    [1, 1, 1, 1, 3, 1, 1],
    [1, 1, 1, 1, 3, 2, 1],
    [1, 1, 1, 3, 2, 1, 0],
    [1, 1, 1, 3, 3, 2, 1],
    [1, 1, 2, 1, 2, 1, 0],
    [1, 1, 2, 1, 2, 2, 1],
    [1, 1, 2, 2, 3, 1, 0],
    [1, 1, 2, 2, 4, 1, 1]
])

string_array = convert_to_strings(array)


def extract_conditions_from_expression(expression):
    conditions, result = expression.split("==>")
    conditions_set = frozenset(re.split(r'\^', conditions.strip()))
    return conditions_set, result.strip()


def filter_unique_combinations(higher_order, lower_order):
    lower_sets = {(conditions, result) for conditions, result in
                  (extract_conditions_from_expression(exp) for exp in lower_order)}

    unique_combinations = []

    for expression in higher_order:
        conditions_set, result = extract_conditions_from_expression(expression)

        is_sub_combination = any(conditions.issubset(conditions_set) and res == result
                                 for conditions, res in lower_sets)

        if not is_sub_combination:
            unique_combinations.append(expression)

    return unique_combinations


def generate_columns(array):
    return [f"a{i+1}" for i in range(array.shape[1] - 1)] + ["d"]

def generate_columns_minus_d(array):
    return [f"a{i+1}" for i in range(array.shape[1] - 1)]


def count_combinations(input_list):
    count_dict = Counter(input_list)

    result = []

    for combination, count in count_dict.items():
        if len(combination) < 15:
            continue

        if count > 1:
            formatted_combination = f"{combination}[{count}]"
        else:
            formatted_combination = f"{combination} "
        result.append(formatted_combination)

    return result

def generate_combinations(columns, count, kount, pominki, pominki2):
    if kount in pominki:
        check_value = pominki2[pominki.index(kount)]
        comb_list = []
        for combo in combinations(columns, count):
            combo_str = "".join(combo)
            if check_value not in combo_str:
                comb_list.append(combo_str)
        return comb_list
    else:
        return ["".join(combo) for combo in combinations(columns, count)]


def check_and_remove_combinations(columns, count, comb_list):
    for combo in combinations(columns, count):
        combo_str = "".join(combo)
        if combo_str in comb_list:
            comb_list.remove(combo_str)


def split_combinations(comb_list):
    split_list = []
    for combo in comb_list:
        split_list.extend([combo[i:i+2] for i in range(0, len(combo), 2)])
    return split_list

def generate_dynamic_answer(split_words, count, j):

    for l in range(0, len(split_words), count):
        term = ''
        for k in range(count):
            if l + k < len(split_words):
                term += f"({split_words[l + k]} = {df[split_words[l + k]].iloc[j]})"
                if k < count - 1:
                    term += "^"
        answer4.append(f"{term} ==> (d = {df[COLUMNS[len(COLUMNS2)]].iloc[j]})")




COLUMNS = generate_columns(array)
COLUMNS2 = COLUMNS[:-1].copy()
key_words = COLUMNS2.copy()
key_words2 = []
key_words3 = []
ans1 = []
answer = []
answer2 = []
answer3 = []
answer4 = []
answer5 = []
answer6 = []
pominki = []
pominki2 = []
previous = ""
counter = 1
df = pd.DataFrame(string_array, columns=COLUMNS)
again = True
again2 = True
first = True


for j in range(len(df)):
    answer.append([])

for i in range(len(df)):
    for k in range(len(df)):
        answer[i].append([])

for u in range(len(df)):
    key_words = COLUMNS2.copy()
    if u == 0:
        for j in range(len(df)):
            key_words = COLUMNS2.copy()
            for i in range(len(df)):
                if i == j:
                    continue
                first_decision = df[COLUMNS[len(COLUMNS2)]].iloc[j]
                second_decision = df[COLUMNS[len(COLUMNS2)]].iloc[i]
                if first_decision == second_decision:
                    continue
                else:
                    for value in COLUMNS2:
                        first_value = df[value].iloc[j]
                        second_value = df[value].iloc[i]
                        if first_value == second_value:
                            answer[i][j].append(f"{value}")
                            if value in key_words:
                                key_words.remove(value)

            if not key_words:
                pass
            else:
                for kk in key_words:
                    answer2.append(f"dla o{j+1} mamy ({kk} = {df[kk].iloc[j]}) ==> (d = {df[COLUMNS[len(COLUMNS2)]].iloc[j]})")
                    answer3.append(f"({kk} = {df[kk].iloc[j]}) ==> (d = {df[COLUMNS[len(COLUMNS2)]].iloc[j]})")
                    pominki.append(j)
                    pominki2.append(kk)

        for i in range(len(answer)):
            print(answer[i])

        for i in answer2:
            print(i)

        print("Reguły postaci:")
        for i in range(len(answer3)):
            if i < len(answer3) - 1:
                if answer3[i] == answer3[i + 1]:
                    counter += 1
                else:
                    if counter > 1:
                        print(f"{answer3[i]}[{counter}]")
                    else:
                        print(f"{answer3[i]}")
            else:
                print(f"{answer3[i]}")

    else:
        for j in range(len(df)):
            key_words2 = generate_combinations(COLUMNS[:-1], u + 1, j, pominki, pominki2)
            for i in range(len(df)):
                if not answer[i][j]:
                    continue
                else:
                    check_and_remove_combinations(answer[i][j], u+1, key_words2)
            if not key_words2:
                pass
            else:
                split_words = split_combinations(key_words2)
                answer4.append(f"z o{j + 1} mamy: ")
                generate_dynamic_answer(split_words, u+1, j)

    for h in range(len(answer4)):
        print(answer4[h])

    for y in answer4:
        if len(y) < 15:
            answer4.remove(y)

    if u % 2 == 1:
        answer5 = answer4
    else:
        answer6 = answer4

    if u > 1:
        if answer4:
            if u % 2 == 1:
                if count_combinations(filter_unique_combinations(answer5, answer6)):
                    print("Reguły postaci:")
                    for t in count_combinations(filter_unique_combinations(answer5, answer6)):
                        print(t)
                else:
                    print(f"Brak reguł postaci")


            else:
                if count_combinations(filter_unique_combinations(answer6, answer5)):
                    print(f"Reguły postaci:")
                    for t in count_combinations(filter_unique_combinations(answer6, answer5)):
                        print(t)
                else:
                    print(f"Brak reguł postaci")


    else:
        if u > 0:
            print(f"Reguły postaci:")

        for i in count_combinations(answer4):
            print(i)

    print("\n")
    answer4 = []



