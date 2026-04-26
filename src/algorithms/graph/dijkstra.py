from typing import Generator, List, Tuple
from src.algorithms.base import BaseAlgorithm
from src.core.events import EventType, AlgorithmEvent


class Dijkstra(BaseAlgorithm):
    """Алгоритм Дейкстры для поиска кратчайших путей во взвешенном графе."""

    _is_completed: bool

    def __init__(self, adj: List[List[Tuple[int, float]]], start: int = 0) -> None:
        super().__init__(list(range(len(adj))))
        self._adj: List[List[Tuple[int, float]]] = adj
        self._start: int = start
        self._dist: List[float] = [float('inf')] * len(adj)
        self._dist[start] = 0.0
        self._visited: List[bool] = [False] * len(adj)

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        n = len(self._adj)
        for _ in range(n):
            u = -1
            min_dist = float('inf')
            for i in range(n):
                yield self._emit(EventType.ACCESS, (i,), (self._dist[i],))
                if not self._visited[i] and self._dist[i] < min_dist:
                    min_dist = self._dist[i]
                    u = i

            if u == -1:
                break

            self._visited[u] = True
            yield self._emit(EventType.NODE_VISITED, (u,), (self._dist[u],))

            for v, weight in self._adj[u]:
                new_dist = self._dist[u] + weight
                yield self._emit(EventType.COMPARE, (u, v), (new_dist, self._dist[v]))
                if new_dist < self._dist[v]:
                    self._dist[v] = new_dist
                    yield self._emit(EventType.PATH_UPDATED, (v,), (self._dist[v],))

        self._is_completed = True
        yield self._emit(EventType.STATE_CHANGE, tuple(range(n)), tuple(self._dist), status="completed")
