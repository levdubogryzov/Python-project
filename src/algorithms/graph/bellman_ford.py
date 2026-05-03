from typing import List, Tuple, Dict, Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError, NegativeCycleError


class BellmanFord(BaseAlgorithm):
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
        self._has_negative_cycle = False
        self._validate_bellman_input()

    def _validate_bellman_input(self) -> None:
        if not self._graph:
            raise InvalidInputError("Граф пуст")
        n = len(self._graph)
        if self._start < 0 or self._start >= n:
            raise InvalidInputError(f"Вершина {self._start} вне диапазона")

    @property
    def distances(self) -> Dict[int, float]:
        return self._distances.copy()

    @property
    def has_negative_cycle(self) -> bool:
        return self._has_negative_cycle

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        n = len(self._graph)
        self._distances = {i: float('inf') for i in range(n)}
        self._distances[self._start] = 0

        edges: List[Tuple[int, int, float]] = []
        for u, neighbors in enumerate(self._graph):
            for v, weight in neighbors:
                edges.append((u, v, weight))

        yield self._emit(
            EventType.VISIT,
            [self._start],
            value=0,
            description=f"Старт из вершины {self._start}",
        )

        for i in range(n - 1):
            updated = False
            for u, v, weight in edges:
                yield self._emit(
                    EventType.RELAX,
                    [u, v],
                    value=weight,
                    description=f"Итерация {i + 1}: ребро {u} -> {v}",
                )

                if self._distances[u] != float('inf'):
                    new_dist = self._distances[u] + weight
                    if new_dist < self._distances[v]:
                        self._distances[v] = new_dist
                        updated = True

            if not updated:
                yield self._emit(
                    EventType.STATE_CHANGE,
                    [],
                    value=i,
                    description=f"Ранняя остановка на итерации {i + 1}",
                )
                break

        for u, v, weight in edges:
            if self._distances[u] != float('inf'):
                if self._distances[u] + weight < self._distances[v]:
                    self._has_negative_cycle = True
                    yield self._emit(
                        EventType.NEGATIVE_CYCLE,
                        [u, v],
                        value=weight,
                        description=f"Отрицательный цикл: {u} -> {v}",
                    )
                    raise NegativeCycleError("Обнаружен отрицательный цикл")
