# Importowanie bibliotek
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from collections import Counter

# Ładowanie danych Iris
iris = load_iris()
X = iris.data
y = iris.target

# Podział na zbiór treningowy i testowy (70% trening, 30% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# Definicje metryk odległości
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b)**2))


def manhattan_distance(a, b):
    return np.sum(np.abs(a - b))


def cosine_distance(a, b):
    return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Implementacja klasyfikatora KNN
def knn_classifier(X_train, y_train, X_test, k, distance_func):
    predictions = []
    for test_point in X_test:
        # Obliczenie dystansów
        distances = [distance_func(test_point, train_point) for train_point in X_train]
        # Znajdowanie k najbliższych sąsiadów
        nearest_indices = np.argsort(distances)[:k]
        nearest_labels = [y_train[i] for i in nearest_indices]
        # Wybór najczęstszej klasy
        most_common_label = Counter(nearest_labels).most_common(1)[0][0]
        predictions.append(most_common_label)
    return predictions


# Ustawienie liczby sąsiadów
k = 3

# Wykonanie klasyfikacji i obliczenie dokładności dla każdej metryki
predictions_euclidean = knn_classifier(X_train, y_train, X_test, k, euclidean_distance)
predictions_manhattan = knn_classifier(X_train, y_train, X_test, k, manhattan_distance)
predictions_cosine = knn_classifier(X_train, y_train, X_test, k, cosine_distance)

accuracy_euclidean = np.mean(predictions_euclidean == y_test)
accuracy_manhattan = np.mean(predictions_manhattan == y_test)
accuracy_cosine = np.mean(predictions_cosine == y_test)

# Wyświetlenie wyników
print(f"Accuracy (Euklidesowa): {accuracy_euclidean:.2f}")
print(f"Accuracy (Manhattan): {accuracy_manhattan:.2f}")
print(f"Accuracy (Cosinusowa): {accuracy_cosine:.2f}")
