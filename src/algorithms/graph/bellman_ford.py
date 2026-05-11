from typing import List, Tuple, Dict, Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError, NegativeCycleError


class BellmanFord(BaseAlgorithm):
    """Алгоритм Беллмана-Форда для поиска кратчайших путей с детектированием отрицательных циклов."""
    def __init__(self, graph: List[List[Tuple[int, float]]], start: int = 0) -> None:
        super().__init__(list(range(len(graph))))
        self._graph = graph
        self._start = start
        self._distances: Dict[int, float] = {i: float('inf') for i in range(len(graph))}
        self._has_negative_cycle = False
        self._validate_bellman_input()

    def _validate_bellman_input(self) -> None:
        """Проверяет входной граф на пустоту и корректность стартовой вершины."""
        if not self._graph:
            raise InvalidInputError("Граф пуст.")
        if not (0 <= self._start < len(self._graph)):
            raise InvalidInputError(f"Вершина {self._start} вне диапазона.")

    @property
    def distances(self) -> Dict[int, float]:
        return self._distances.copy()

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Запускает итерационный процесс релаксации ребер и поиска отрицательных циклов."""
        n = len(self._graph)
        self._distances = {i: float('inf') for i in range(n)}
        self._distances[self._start] = 0.0

        for node_idx, dist in self._distances.items():
            yield self._emit(
                event_type=EventType.UPDATE,
                indices=[node_idx],
                value=dist,
                description=f"Инициализация: {node_idx} = {dist}"
            )

        edges: List[Tuple[int, int, float]] = []
        for u, neighbors in enumerate(self._graph):
            for v, weight in neighbors:
                edges.append((u, v, weight))

        for i in range(n - 1):
            any_update = False
            for u, v, weight in edges:
                yield self._emit(
                    event_type=EventType.RELAX,
                    indices=[u, v],
                    value=weight,
                    description=f"Итерация {i + 1}: проверка ребра {u} -> {v}"
                )

                if self._distances[u] != float('inf'):
                    new_dist = self._distances[u] + weight
                    if new_dist < self._distances[v]:
                        self._distances[v] = new_dist
                        any_update = True
                        yield self._emit(
                            event_type=EventType.UPDATE,
                            indices=[v],
                            value=self._distances[v],
                            description=f"Обновлено расстояние до {v}: {new_dist}"
                        )
            if not any_update:
                break

        for u, v, weight in edges:
            if self._distances[u] != float('inf') and self._distances[u] + weight < self._distances[v]:
                yield self._emit(
                    event_type=EventType.NEGATIVE_CYCLE,
                    indices=[u, v],
                    description="Найден отрицательный цикл!"
                )
                raise NegativeCycleError("Граф содержит отрицательный цикл")
