import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from collections import Counter

iris = load_iris()
dane = iris.data
etykiety = iris.target

dane_trening, dane_test, etykiety_trening, etykiety_test = train_test_split(
    dane, etykiety, test_size=0.3, random_state=42
)

def odleglosc_euklidesowa(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def odleglosc_manhattan(a, b):
    return np.sum(np.abs(a - b))

def odleglosc_cosinusowa(a, b):
    return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def klasyfikator_knn(dane_trening, etykiety_trening, dane_test, k, funkcja_odleglosci):
    przewidywania = []
    for punkt_testowy in dane_test:
        odleglosci = [
            funkcja_odleglosci(punkt_testowy, punkt_treningowy)
            for punkt_treningowy in dane_trening
        ]
        najblizsze_indeksy = np.argsort(odleglosci)[:k]
        najblizsze_etykiety = [etykiety_trening[i] for i in najblizsze_indeksy]
        najczestsza_etykieta = Counter(najblizsze_etykiety).most_common(1)[0][0]
        przewidywania.append(najczestsza_etykieta)
    return przewidywania

k = 3

przewidywania_euklides = klasyfikator_knn(
    dane_trening, etykiety_trening, dane_test, k, odleglosc_euklidesowa
)
przewidywania_manhattan = klasyfikator_knn(
    dane_trening, etykiety_trening, dane_test, k, odleglosc_manhattan
)
przewidywania_cosinus = klasyfikator_knn(
    dane_trening, etykiety_trening, dane_test, k, odleglosc_cosinusowa
)

dokladnosc_euklides = np.mean(przewidywania_euklides == etykiety_test)
dokladnosc_manhattan = np.mean(przewidywania_manhattan == etykiety_test)
dokladnosc_cosinus = np.mean(przewidywania_cosinus == etykiety_test)

print(f"Dokładność (Euklidesowa): {dokladnosc_euklides:.2f}")
print(f"Dokładność (Manhattan): {dokladnosc_manhattan:.2f}")
print(f"Dokładność (Cosinusowa): {dokladnosc_cosinus:.2f}")
