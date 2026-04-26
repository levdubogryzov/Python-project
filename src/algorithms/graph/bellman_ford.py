from typing import Generator, List, Tuple
from src.algorithms.base import BaseAlgorithm
from src.core.events import EventType, AlgorithmEvent


class BellmanFord(BaseAlgorithm):
    """Алгоритм Беллмана-Форда для поиска кратчайших путей с поддержкой отрицательных весов."""

    _is_completed: bool

    def __init__(self, adj: List[List[Tuple[int, float]]], start: int = 0) -> None:
        n = len(adj)
        super().__init__(list(range(n)))
        self._adj: List[List[Tuple[int, float]]] = adj
        self._start: int = start
        self._dist: List[float] = [float('inf')] * n
        self._dist[start] = 0.0

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        n = len(self._adj)
        edges = []
        for u in range(n):
            for v, w in self._adj[u]:
                edges.append((u, v, w))

        for _ in range(n - 1):
            updated = False
            for u, v, w in edges:
                if self._dist[u] != float('inf'):
                    yield self._emit(EventType.ACCESS, (u, v), (self._dist[u], self._dist[v]))
                    new_dist = self._dist[u] + w
                    yield self._emit(EventType.COMPARE, (u, v), (new_dist, self._dist[v]))
                    if new_dist < self._dist[v]:
                        self._dist[v] = new_dist
                        yield self._emit(EventType.PATH_UPDATED, (v,), (self._dist[v],))
                        updated = True
            if not updated:
                break

        for u, v, w in edges:
            if self._dist[u] != float('inf') and self._dist[u] + w < self._dist[v]:
                yield self._emit(EventType.STATE_CHANGE, (), (), status="negative_cycle")
                self._is_completed = True
                return

        self._is_completed = True
        yield self._emit(EventType.STATE_CHANGE, tuple(range(n)), tuple(self._dist), status="completed")
