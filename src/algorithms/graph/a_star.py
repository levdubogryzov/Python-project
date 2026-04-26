from typing import Generator, List, Tuple, Callable, Set
import heapq
from src.algorithms.base import BaseAlgorithm
from src.core.events import EventType, AlgorithmEvent


class AStar(BaseAlgorithm):
    """Алгоритм A* для поиска кратчайших путей с эвристикой."""

    _is_completed: bool

    def __init__(self, adj: List[List[Tuple[int, float]]], start: int = 0, end: int = -1,
                 heuristic: Callable[[int, int], float] = lambda u, v: 0.0) -> None:
        n = len(adj)
        super().__init__(list(range(n)))
        self._adj: List[List[Tuple[int, float]]] = adj
        self._start: int = start
        self._end: int = n - 1 if end == -1 else end
        self._heuristic: Callable[[int, int], float] = heuristic
        self._dist: List[float] = [float('inf')] * n
        self._dist[start] = 0.0
        self._f_score: List[float] = [float('inf')] * n
        self._f_score[start] = self._heuristic(start, self._end)

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        n = len(self._adj)
        open_set = [(self._f_score[self._start], self._start)]
        in_open_set: Set[int] = {self._start}

        while open_set:
            _, u = heapq.heappop(open_set)
            in_open_set.discard(u)

            if u == self._end:
                break

            yield self._emit(EventType.NODE_VISITED, (u,), (self._dist[u],))

            for v, weight in self._adj[u]:
                yield self._emit(EventType.ACCESS, (v,), (self._dist[v],))
                new_dist = self._dist[u] + weight
                yield self._emit(EventType.COMPARE, (u, v), (new_dist, self._dist[v]))
                if new_dist < self._dist[v]:
                    self._dist[v] = new_dist
                    self._f_score[v] = new_dist + self._heuristic(v, self._end)
                    yield self._emit(EventType.PATH_UPDATED, (v,), (self._dist[v],))
                    if v not in in_open_set:
                        heapq.heappush(open_set, (self._f_score[v], v))
                        in_open_set.add(v)

        self._is_completed = True
        yield self._emit(EventType.STATE_CHANGE, tuple(range(n)), tuple(self._dist), status="completed")
