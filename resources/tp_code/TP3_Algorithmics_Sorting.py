"""
TP 3: Algorithmiques - Analyse de Complexité et Optimisation
EST Guelmim - Algorithmiques
Auteur: Nour Eddine AIT ABDALLAH

Objectif: Implémenter différents algorithmes de tri et analyser leur complexité
"""

import time
import random
from typing import List, Tuple

class SortingAnalyzer:
    """Classe pour analyser les algorithmes de tri"""
    
    @staticmethod
    def bubble_sort(arr: List[int]) -> Tuple[List[int], int]:
        """
        Tri par bulle - O(n²)
        """
        n = len(arr)
        comparisons = 0
        arr = arr.copy()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        return arr, comparisons
    
    @staticmethod
    def insertion_sort(arr: List[int]) -> Tuple[List[int], int]:
        """
        Tri par insertion - O(n²)
        Meilleur que bubble_sort en pratique
        """
        n = len(arr)
        comparisons = 0
        arr = arr.copy()
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            while j >= 0:
                comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    j -= 1
                else:
                    break
            
            arr[j + 1] = key
        
        return arr, comparisons
    
    @staticmethod
    def merge_sort(arr: List[int]) -> Tuple[List[int], int]:
        """
        Tri fusion - O(n log n)
        Bien plus rapide pour grandes listes
        """
        comparisons = [0]  # Utiliser une liste pour modifier dans les fonctions imbriquées
        
        def merge(left, right):
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                comparisons[0] += 1
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def sort(arr):
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left = sort(arr[:mid])
            right = sort(arr[mid:])
            
            return merge(left, right)
        
        return sort(arr), comparisons[0]
    
    @staticmethod
    def quick_sort(arr: List[int]) -> Tuple[List[int], int]:
        """
        Tri rapide - O(n log n) en moyenne, O(n²) pire cas
        Plus rapide que merge_sort en pratique
        """
        comparisons = [0]
        
        def partition(low, high):
            pivot = arr[high]
            i = low - 1
            
            for j in range(low, high):
                comparisons[0] += 1
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1
        
        def sort(low, high):
            if low < high:
                pi = partition(low, high)
                sort(low, pi - 1)
                sort(pi + 1, high)
        
        arr = arr.copy()
        sort(0, len(arr) - 1)
        return arr, comparisons[0]
    
    @staticmethod
    def benchmark(algorithm, arr: List[int], name: str):
        """
        Benchmark un algorithme de tri
        """
        start_time = time.time()
        sorted_arr, comparisons = algorithm(arr)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # en millisecondes
        
        print(f"\n{name}:")
        print(f"  Comparaisons: {comparisons:,}")
        print(f"  Temps d'exécution: {execution_time:.4f} ms")
        
        return execution_time


def main():
    """Démonstration comparative des algorithmes de tri"""
    
    print("="*60)
    print("ANALYSE DE COMPLEXITÉ - ALGORITHMES DE TRI")
    print("EST Guelmim - Algorithmiques")
    print("="*60)
    
    # Tester avec différentes tailles
    sizes = [100, 1000, 5000]
    
    for size in sizes:
        print(f"\n{'='*60}")
        print(f"Taille du tableau: {size} éléments")
        print("="*60)
        
        # Générer un tableau aléatoire
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        analyzer = SortingAnalyzer()
        
        # Bubble Sort
        analyzer.benchmark(analyzer.bubble_sort, arr, "Tri par Bulle O(n²)")
        
        # Insertion Sort
        analyzer.benchmark(analyzer.insertion_sort, arr, "Tri par Insertion O(n²)")
        
        # Merge Sort
        analyzer.benchmark(analyzer.merge_sort, arr, "Tri Fusion O(n log n)")
        
        # Quick Sort
        analyzer.benchmark(analyzer.quick_sort, arr, "Tri Rapide O(n log n)")
        
        # Tri natif Python
        start = time.time()
        sorted_arr = sorted(arr)
        end = time.time()
        print(f"\nTri natif Python (Timsort):")
        print(f"  Temps d'exécution: {(end - start) * 1000:.4f} ms")
    
    # Analyse théorique
    print(f"\n{'='*60}")
    print("ANALYSE THÉORIQUE DE COMPLEXITÉ")
    print("="*60)
    
    print("""
Complexité Temporelle:
- Bubble Sort: O(n²) pire cas, O(n²) cas moyen
- Insertion Sort: O(n²) pire cas, O(n) meilleur cas
- Merge Sort: O(n log n) tous les cas
- Quick Sort: O(n²) pire cas, O(n log n) cas moyen
- Timsort: O(n log n) tous les cas (hybride merge+insertion)

Complexité Spatiale:
- Bubble Sort: O(1)
- Insertion Sort: O(1)
- Merge Sort: O(n)
- Quick Sort: O(log n) récursion
- Timsort: O(n)

Recommandations:
✓ Petites listes (n < 100): Insertion Sort
✓ Listes générales: Quick Sort ou Timsort
✓ Données presque triées: Timsort
✓ Cas où stabilité requise: Merge Sort
    """)


if __name__ == "__main__":
    main()
