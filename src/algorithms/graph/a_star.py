from typing import List, Tuple, Dict, Generator, Set, Optional, Callable
import heapq
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError


class AStar(BaseAlgorithm):
    def __init__(
            self,
            graph: List[List[Tuple[int, float]]],
            start: int = 0,
            end: Optional[int] = None,
            heuristic: Optional[Callable[[int, int], float]] = None,
    ) -> None:
        vertices = list(range(len(graph)))
        super().__init__(vertices)

        self._graph = graph
        self._start = start
        self._end = end if end is not None else len(graph) - 1
        self._heuristic = heuristic or (lambda x, y: 0)
        self._distances: Dict[int, float] = {}
        self._validate_astar_input()

    def _validate_astar_input(self) -> None:
        if not self._graph:
            raise InvalidInputError("Граф пуст")
        n = len(self._graph)
        if self._start < 0 or self._start >= n:
            raise InvalidInputError(f"Вершина {self._start} вне диапазона")
        if self._end < 0 or self._end >= n:
            raise InvalidInputError(f"Вершина {self._end} вне диапазона")

        for u, neighbors in enumerate(self._graph):
            for v, weight in neighbors:
                if weight < 0:
                    raise InvalidInputError(f"Отрицательный вес ребра {u}->{v}. Используйте Bellman-Ford.")
                if v < 0 or v >= n:
                    raise InvalidInputError(f"Некорректная вершина {v}")

    @property
    def distances(self) -> Dict[int, float]:
        return self._distances.copy()

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        n = len(self._graph)
        self._distances = {i: float('inf') for i in range(n)}
        self._distances[self._start] = 0

        g_score: Dict[int, float] = {self._start: 0}
        visited: Set[int] = set()
        pq: List[Tuple[float, int]] = [(0, self._start)]

        yield self._emit(
            EventType.VISIT,
            [self._start],
            value=0,
            description=f"Старт из вершины {self._start}",
        )

        while pq:
            f, u = heapq.heappop(pq)

            if u in visited:
                continue

            visited.add(u)
            self._distances[u] = g_score[u]

            h = self._heuristic(u, self._end)
            yield self._emit(
                EventType.HEURISTIC,
                [u],
                value=h,
                description=f"Эвристика h({u}) = {h}",
            )

            if u == self._end:
                yield self._emit(
                    EventType.FOUND,
                    [u],
                    value=self._distances[u],
                    description=f"Цель достигнута: вершина {self._end}",
                )
                break

            for v, weight in self._graph[u]:
                if v in visited:
                    continue

                yield self._emit(
                    EventType.COMPARE,
                    [u, v],
                    value=weight,
                    description=f"Ребро {u}->{v}, вес {weight}",
                )

                new_g = g_score[u] + weight
                if new_g < g_score.get(v, float('inf')):
                    g_score[v] = new_g
                    f_score = new_g + self._heuristic(v, self._end)

                    yield self._emit(
                        EventType.RELAX,
                        [u, v],
                        value=new_g,
                        description=f"Релаксация {u}->{v}: g={new_g}",
                    )
                    heapq.heappush(pq, (f_score, v))
