from typing import List, Tuple
from src.algorithms.base import BaseAlgorithm
from src.algorithms.sorting.shell import ShellSort
from src.algorithms.sorting.quick import QuickSort
from src.algorithms.sorting.merge import MergeSort
from src.algorithms.graph.dijkstra import Dijkstra
from src.algorithms.graph.a_star import AStar
from src.algorithms.graph.bellman_ford import BellmanFord
from src.validation.validator import AlgorithmValidator
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def run_validation(
    algo_name: str,
    algo_instance: BaseAlgorithm,
) -> None:
    """Запускает алгоритм сортировки и проверяет результат."""
    print(f"\nТест: {algo_name}")
    list(algo_instance.run())
    validator = AlgorithmValidator()

    is_valid = validator.validate_sorting(list(algo_instance.run()), algo_instance.data)
    if is_valid:
        print(f"[OK] {algo_name} прошёл валидацию. Шагов: {algo_instance.steps_count}")
    else:
        print(f"[FAIL] {algo_name} провалил валидацию:")
        for err in validator.errors:
            print(f"   - {err}")


def run_graph_test(algo_name: str, algo_instance: BaseAlgorithm) -> None:
    """Запускает графовый алгоритм и выводит результаты."""
    print(f"\nТест: {algo_name}")
    try:
        list(algo_instance.run())
        print(f"[OK] {algo_name} выполнен. Шагов: {algo_instance.steps_count}")
        print(f"    Результат: {algo_instance.data}")
    except Exception as exc:
        print(f"[FAIL] {algo_name} завершился с ошибкой: {exc}")


def main() -> None:
    """Точка входа для демонстрации работы ядра."""
    test_data: List[int] = [64, 34, 25, 12, 22, 11, 90, 4, 5, 2, 0]

    run_validation("ShellSort", ShellSort(test_data.copy()))
    run_validation("QuickSort", QuickSort(test_data.copy()))
    run_validation("MergeSort", MergeSort(test_data.copy()))

    graph: List[List[Tuple[int, float]]] = [
        [(1, 4), (2, 1)],
        [(3, 1)],
        [(1, 2), (3, 5)],
        [],
    ]

    run_graph_test("Dijkstra", Dijkstra(graph, start=0))
    run_graph_test("BellmanFord", BellmanFord(graph, start=0))
    run_graph_test("AStar", AStar(graph, start=0, end=3))

    print("\nЯдро готово к подключению Manim-рендерера!")


if __name__ == "__main__":
    main()
