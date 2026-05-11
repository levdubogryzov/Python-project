from typing import List, Tuple, Dict, Generator, Set, Optional, Callable
import heapq
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError


class AStar(BaseAlgorithm):
    """Алгоритм A* для поиска кратчайшего пути с использованием эвристической функции."""
    def __init__(
            self,
            graph: List[List[Tuple[int, float]]],
            start: int = 0,
            end: Optional[int] = None,
            heuristic: Optional[Callable[[int, int], float]] = None,
    ) -> None:
        super().__init__(list(range(len(graph))))
        self._graph = graph
        self._start = start
        self._end = end if end is not None else len(graph) - 1
        self._heuristic = heuristic or (lambda x, y: 0.0)
        self._distances: Dict[int, float] = {i: float('inf') for i in range(len(graph))}
        self._validate_astar_input()

    def _validate_astar_input(self) -> None:
        """Проверяет корректность графа, начальной и конечной точек."""
        if not self._graph:
            raise InvalidInputError("Граф пуст.")
        n = len(self._graph)
        if not (0 <= self._start < n) or not (0 <= self._end < n):
            raise InvalidInputError("Начальная или конечная вершина вне диапазона.")
        for u, neighbors in enumerate(self._graph):
            for v, weight in neighbors:
                if weight < 0:
                    raise InvalidInputError(f"Отрицательный вес {weight} у ребра {u}->{v}.")

    @property
    def distances(self) -> Dict[int, float]:
        return self._distances.copy()

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Выполняет поиск пути, генерируя события обновления стоимостей и посещения узлов."""
        n = len(self._graph)
        self._distances = {i: float('inf') for i in range(n)}

        for node_idx, dist in self._distances.items():
            yield self._emit(
                event_type=EventType.UPDATE,
                indices=[node_idx],
                value=dist,
                description=f"Инициализация: {node_idx}"
            )

        g_score: Dict[int, float] = {self._start: 0.0}
        visited: Set[int] = set()
        pq: List[Tuple[float, int]] = [(0.0, self._start)]

        yield self._emit(
            event_type=EventType.VISIT,
            indices=[self._start],
            value=0.0,
            description=f"Старт поиска из вершины {self._start}"
        )

        while pq:
            f, u = heapq.heappop(pq)
            if u in visited:
                continue

            visited.add(u)
            self._distances[u] = g_score[u]

            yield self._emit(
                event_type=EventType.UPDATE,
                indices=[u],
                value=g_score[u],
                description=f"Посещена вершина {u}, g={g_score[u]}"
            )

            if u == self._end:
                yield self._emit(
                    event_type=EventType.STATE_CHANGE,
                    indices=[u],
                    description=f"Путь найден! Дистанция: {self._distances[u]}"
                )
                break

            for v, weight in self._graph[u]:
                if v in visited:
                    continue

                yield self._emit(
                    event_type=EventType.RELAX,
                    indices=[u, v],
                    value=weight,
                    description=f"Проверка ребра {u} -> {v}"
                )

                new_g = g_score[u] + weight
                if new_g < g_score.get(v, float('inf')):
                    g_score[v] = new_g
                    f_score = new_g + self._heuristic(v, self._end)
                    yield self._emit(
                        event_type=EventType.UPDATE,
                        indices=[v],
                        value=new_g,
                        description=f"Новый путь до {v}: {new_g}"
                    )
                    heapq.heappush(pq, (f_score, v))
