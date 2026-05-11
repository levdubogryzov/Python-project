from typing import List, Tuple, Dict, Generator, Set
import heapq
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError


class Dijkstra(BaseAlgorithm):
    """Алгоритм Дейкстры для поиска кратчайших путей с генерацией событий визуализации."""

    def __init__(self, graph: List[List[Tuple[int, float]]], start: int = 0) -> None:
        """Инициализирует граф, начальную вершину и валидирует входные данные."""
        super().__init__(list(range(len(graph))))
        self._graph = graph
        self._start = start
        self._distances: Dict[int, float] = {i: float('inf') for i in range(len(graph))}
        self._validate_dijkstra_input()

    def _validate_dijkstra_input(self) -> None:
        """Проверяет граф на отсутствие отрицательных весов и корректность индексов."""
        if not self._graph:
            raise InvalidInputError("Граф пуст.")
        n = len(self._graph)
        if not (0 <= self._start < n):
            raise InvalidInputError(f"Вершина {self._start} вне диапазона.")

        for u, neighbors in enumerate(self._graph):
            for v, weight in neighbors:
                if weight < 0:
                    raise InvalidInputError(f"Отрицательный вес ребра {u}->{v}.")
                if not (0 <= v < n):
                    raise InvalidInputError(f"Некорректная вершина {v}.")

    @property
    def distances(self) -> Dict[int, float]:
        """Возвращает копию текущего словаря кратчайших расстояний."""
        return self._distances.copy()

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Выполняет расчет путей, пошагово генерируя события посещения и релаксации."""
        n = len(self._graph)
        self._distances = {i: float('inf') for i in range(n)}
        self._distances[self._start] = 0.0

        for node_idx, dist in self._distances.items():
            yield self._emit(
                event_type=EventType.UPDATE,
                indices=[node_idx],
                value=dist,
                description=f"Инициализация: {node_idx}"
            )

        visited: Set[int] = set()
        pq: List[Tuple[float, int]] = [(0.0, self._start)]

        while pq:
            dist, u = heapq.heappop(pq)

            if u in visited:
                continue

            visited.add(u)
            yield self._emit(
                event_type=EventType.VISIT,
                indices=[u],
                value=dist,
                description=f"Посещена вершина {u}, путь: {dist}"
            )

            for v, weight in self._graph[u]:
                yield self._emit(
                    event_type=EventType.RELAX,
                    indices=[u, v],
                    value=weight,
                    description=f"Проверка ребра {u} -> {v}"
                )

                if v not in visited:
                    new_dist = dist + weight
                    if new_dist < self._distances[v]:
                        self._distances[v] = new_dist
                        yield self._emit(
                            event_type=EventType.UPDATE,
                            indices=[v],
                            value=new_dist,
                            description=f"Обновлено расстояние до {v}: {new_dist}"
                        )
                        heapq.heappush(pq, (new_dist, v))
