from typing import List, Tuple, Dict, Generator, Set
import heapq
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError


class Dijkstra(BaseAlgorithm):
    def __init__(
            self,
            graph: List[List[Tuple[int, float]]],
            start: int = 0,
    ) -> None:
        vertices = list(range(len(graph)))
        super().__init__(vertices)

        self._graph = graph
        self._start = start
        self._distances: Dict[int, float] = {}
        self._validate_dijkstra_input()

    def _validate_dijkstra_input(self) -> None:
        if not self._graph:
            raise InvalidInputError("Граф пуст")
        n = len(self._graph)
        if self._start < 0 or self._start >= n:
            raise InvalidInputError(f"Вершина {self._start} вне диапазона")
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
        visited: Set[int] = set()
        pq: List[Tuple[float, int]] = [(0, self._start)]

        yield self._emit(
            EventType.VISIT,
            [self._start],
            value=0,
            description=f"Старт из вершины {self._start}",
        )

        while pq:
            dist, u = heapq.heappop(pq)

            if u in visited:
                continue

            visited.add(u)

            yield self._emit(
                EventType.VISIT,
                [u],
                value=dist,
                description=f"Посещена вершина {u}, расстояние {dist}",
            )

            for v, weight in self._graph[u]:
                yield self._emit(
                    EventType.COMPARE,
                    [u, v],
                    value=weight,
                    description=f"Ребро {u}->{v}, вес {weight}",
                )

                if v not in visited:
                    new_dist = dist + weight
                    if new_dist < self._distances[v]:
                        self._distances[v] = new_dist
                        yield self._emit(
                            EventType.RELAX,
                            [u, v],
                            value=new_dist,
                            description=f"Релаксация {u}->{v}: {new_dist}",
                        )
                        heapq.heappush(pq, (new_dist, v))
