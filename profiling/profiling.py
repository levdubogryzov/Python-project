from __future__ import annotations
import cProfile
import pstats
import io
import time
import sys
import tracemalloc
from typing import Any
from src.algorithms.sorting.quick import QuickSort
from src.algorithms.sorting.merge import MergeSort
from src.algorithms.sorting.shell import ShellSort
from src.algorithms.graph.dijkstra import Dijkstra
from src.algorithms.graph.bellman_ford import BellmanFord
from src.algorithms.graph.a_star import AStar
from config import ProjectConfig
from src.core.events import AlgorithmEvent, EventType


def run_and_timer(algo: Any) -> tuple[list[Any], float, float]:
    tracemalloc.start()
    start = time.perf_counter()

    events = list(algo.run())

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return events, end - start, peak / 1024


def profile_expanded() -> None:
    cfg = ProjectConfig()
    test_data_large = list(range(200, 0, -1))
    graph = cfg.DEFAULT_GRAPH

    algos = [
        ("QuickSort (N=200)", QuickSort(test_data_large.copy())),
        ("MergeSort (N=200)", MergeSort(test_data_large.copy())),
        ("ShellSort (N=200)", ShellSort(test_data_large.copy())),
        ("Dijkstra", Dijkstra(graph, start=cfg.DEFAULT_GRAPH_START)),
        ("Bellman-Ford", BellmanFord(graph, start=cfg.DEFAULT_GRAPH_START)),
        ("A*", AStar(graph, start=cfg.DEFAULT_GRAPH_START, end=cfg.DEFAULT_GRAPH_END))
    ]

    print(f"{'Algorithm':<20} | {'Events':<7} | {'Time (s)':<10} | {'ms/Evt':<8} | {'Peak (KB)':<10}")
    print("-" * 70)

    for name, algo in algos:
        events, duration, peak_kb = run_and_timer(algo)
        ms_per_event = (duration / len(events) * 1000) if events else 0
        print(f"{name:<20} | {len(events):<7} | {duration:<10.4f} | {ms_per_event:<8.3f} | {peak_kb:<10.2f}")

    print("\n" + "=" * 60)
    print("ДЕТАЛИЗАЦИЯ ВЫЗОВОВ (TOP 20 CUMULATIVE TIME)")
    print("=" * 60)

    pr = cProfile.Profile()
    pr.enable()
    for _ in range(100):
        list(QuickSort(list(range(50, 0, -1))).run())
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(20)
    print(s.getvalue())

    sample_event = AlgorithmEvent(event_type=EventType.COMPARE, indices=[0, 1])
    event_size = sys.getsizeof(sample_event)
    print("=" * 60)
    print(f"Анализ объектов: Размер одного AlgorithmEvent ~{event_size} bytes")
    print(f"Использование генераторов обеспечивает сложность по памяти O(1)")
    print("=" * 60)


if __name__ == "__main__":
    profile_expanded()
