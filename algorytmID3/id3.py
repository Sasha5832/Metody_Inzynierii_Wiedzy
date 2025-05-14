#!/usr/bin/env python3
"""
Pure Python implementation of the ID3 decision‑tree learning algorithm.

Requirements
------------
* standard‑library only (csv, math, argparse…)
* a plain‑text file whose first line zawiera nazwy atrybutów,
  ostatnia kolumna to atrybut decyzyjny (lub wskaż go przełącznikiem --target)

Usage
-----
Train and print the tree:

    python id3.py SystemDecyzyjny.txt

Verbose mode (pokaż każde obliczenie zysku informacyjnego):

    python id3.py SystemDecyzyjny.txt -v
"""
import argparse, csv, math, sys
from collections import Counter, defaultdict
from pathlib import Path

# ───────────────────────── pomocnicze funkcje ──────────────────────────
def entropy(examples, target):
    total = len(examples)
    counts = Counter(r[target] for r in examples)
    return -sum((c/total)*math.log2(c/total) for c in counts.values())

def split(examples, attr):
    parts = defaultdict(list)
    for row in examples:
        parts[row[attr]].append(row)
    return parts

def gain(examples, attr, target):
    parent = entropy(examples, target)
    total  = len(examples)
    weighted = sum((len(s)/total)*entropy(s, target) for s in split(examples, attr).values())
    return parent - weighted      # definicja zysku informacyjnego :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

def majority(examples, target):
    return Counter(r[target] for r in examples).most_common(1)[0][0]

# ───────────────────────── struktura drzewa ────────────────────────────


class Node:                       # węzeł lub liść
    __slots__ = ("attribute", "label", "branches")

    def __init__(self, *, attribute=None, label=None):
        self.attribute = attribute
        self.label = label
        self.branches = {}

    def pretty(self, indent=""):
        if self.label is not None:
            return indent + f"[class: {self.label}]"
        lines = []
        for v, child in self.branches.items():
            lines.append(indent + f"{self.attribute} = {v}:")
            lines.append(child.pretty(indent + "  "))
        return "\n".join(lines)

    def classify(self, sample):   # uproszczona klasyfikacja nowego obiektu
        return self.label if self.label is not None else \
               self.branches.get(sample.get(self.attribute),
                                  next(iter(self.branches.values()))).classify(sample)

# ─────────────────────────── algorytm ID3 ──────────────────────────────
def id3(examples, attributes, target, *, depth=0, verbose=False):
    first = examples[0][target]
    if all(r[target] == first for r in examples):         # 1. wszystkie w tej samej klasie
        return Node(label=first)
    if not attributes:                                   # 2. brak atrybutów → liść majority
        return Node(label=majority(examples, target))

    # 3. wybierz atrybut o największym Gain
    gains = [(gain(examples, a, target), a) for a in attributes]
    best_gain, best_attr = max(gains, key=lambda x: x[0])

    if verbose:
        pad = "│   " * depth
        print(pad + "Gain:")
        for g, a in sorted(gains, reverse=True): print(pad + f"  {a:<20} {g:.4f}")
        print(pad + f"→ Split on '{best_attr}' (gain={best_gain:.4f})\n")

    if best_gain == 0:                                   # 4. brak informacji → liść majority
        return Node(label=majority(examples, target))

    node      = Node(attribute=best_attr)
    remain    = [a for a in attributes if a != best_attr]
    for v, sub in split(examples, best_attr).items():    # rekurencja
        node.branches[v] = id3(sub, remain, target, depth=depth+1, verbose=verbose)
    return node

# ─────────────────────────── wczytywanie danych ───────────────────────
def sniff(path: Path):
    sample = path.open(encoding="utf-8").read(4096)
    try:  return csv.Sniffer().sniff(sample)
    except csv.Error:
        class Tab(csv.excel): delimiter = "\t"
        return Tab

def load(path: Path, *, target=None):
    dialect = sniff(path)
    rows    = list(csv.reader(path.open(encoding="utf-8"), dialect))
    if not rows: raise ValueError("Pusty plik!")
    headers = rows[0]
    if target is None: target = headers[-1]
    examples   = [dict(zip(headers, r)) for r in rows[1:] if len(r) == len(headers)]
    attributes = [h for h in headers if h != target]
    return examples, attributes, target

# ─────────────────────────── uruchomienie │ CLI ───────────────────────
def main():
    p = argparse.ArgumentParser(description="ID3 decision‑tree learner (pure‑python)")
    p.add_argument("datafile", type=Path)
    p.add_argument("-t", "--target", metavar="ATTR")
    p.add_argument("-v", "--verbose", action="store_true", help="pokaż obliczenia Gain")
    p.add_argument("--interactive", action="store_true",
                   help="na końcu pozwól ręcznie klasyfikować nowe obiekty")
    args = p.parse_args()

    examples, attrs, target = load(args.datafile, target=args.target)
    tree = id3(examples, attrs, target, verbose=args.verbose)

    print("\nWygenerowane drzewo decyzyjne:")
    print(tree.pretty())

    if args.interactive:
        print("\nWpisuj wartości atrybutów (oddzielone przecinkami) – Ctrl‑D aby zakończyć:")
        order = attrs.copy()
        try:
            while True:
                line = input(f"{', '.join(order)} = ").strip()
                if not line: continue
                vals = [v.strip() for v in line.split(",")]
                if len(vals) != len(order):
                    print("✖ Liczba wartości nie zgadza się!")
                    continue
                print("→ Klasa:", tree.classify(dict(zip(order, vals))))
        except (EOFError, KeyboardInterrupt):
            pass

if __name__ == "__main__":
    main()
