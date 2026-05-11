from __future__ import annotations
from copy import deepcopy
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import EventProtocolError


class AlgorithmValidator:
    """Класс для проверки корректности потока событий и итоговых данных."""

    ALLOWED_SORTING_EVENTS: set[EventType] = {
        EventType.COMPARE, EventType.SWAP, EventType.ACCESS,
        EventType.OVERWRITE, EventType.STATE_CHANGE, EventType.PARTITION,
        EventType.MERGE, EventType.SPLIT, EventType.PIVOT, EventType.VISIT,
    }

    ALLOWED_GRAPH_EVENTS: set[EventType] = {
        EventType.VISIT, EventType.UPDATE, EventType.RELAX,
        EventType.HEURISTIC, EventType.NEGATIVE_CYCLE, EventType.FOUND,
    }

    def __init__(self) -> None:
        self._errors: list[str] = []

    def validate_sorting(self, events: list[AlgorithmEvent], initial_data: list[int]) -> bool:
        """Проверяет последовательность событий сортировки и финальное состояние массива."""
        self._errors.clear()
        mirror_data = deepcopy(initial_data)

        try:
            self._validate_events(events, self.ALLOWED_SORTING_EVENTS, mirror_data)
        except (EventProtocolError, IndexError) as exc:
            self._errors.append(str(exc))
            return False

        if not self._is_sorted(mirror_data):
            self._errors.append("Конечные данные не отсортированы.")
            return False
        return True

    def validate_graph(self, distances: dict[int, float], graph: list[list[tuple[int, float]]], start: int) -> bool:
        """Проверяет корректность вычисленных кратчайших путей в графе."""
        self._errors.clear()
        num_vertices = len(graph)

        if not isinstance(distances, dict):
            self._errors.append("Расстояния должны быть словарем.")
            return False

        if not (0 <= start < num_vertices):
            self._errors.append(f"Некорректная стартовая вершина: {start}")
            return False

        if len(distances) != num_vertices:
            self._errors.append(f"Несоответствие количества вершин: {len(distances)} != {num_vertices}")
            return False

        if distances.get(start, float('inf')) != 0:
            self._errors.append("Расстояние до стартовой вершины должно быть 0.")
            return False

        for u in range(num_vertices):
            u_dist = distances.get(u, float('inf'))
            if u_dist == float('inf'):
                continue

            for v, weight in graph[u]:
                v_dist = distances.get(v, float('inf'))
                if v_dist > u_dist + weight + 1e-9:
                    self._errors.append(f"Нарушение оптимальности для ребра {u}->{v}")
                    return False
        return True

    @staticmethod
    def _is_sorted(data: list[int]) -> bool:
        """Проверяет, отсортирован ли список по возрастанию."""
        return all(data[i] <= data[i + 1] for i in range(len(data) - 1))

    @staticmethod
    def _validate_events(events: list[AlgorithmEvent], allowed: set[EventType], mirror_data: list[Any]) -> None:
        """Проверяет типы событий и имитирует изменения в зеркальном массиве."""
        for idx, evt in enumerate(events):
            if evt.type not in allowed:
                raise EventProtocolError(f"Тип '{evt.type}' запрещен на шаге {idx}")

            for i in evt.indices:
                if not (0 <= i < len(mirror_data)):
                    raise IndexError(f"Индекс {i} вне диапазона на шаге {idx}")

            if evt.type == EventType.SWAP:
                if len(evt.indices) != 2:
                    raise EventProtocolError(f"SWAP требует 2 индекса на шаге {idx}")
                i, j = evt.indices[0], evt.indices[1]
                mirror_data[i], mirror_data[j] = mirror_data[j], mirror_data[i]

            elif evt.type == EventType.OVERWRITE:
                if not evt.indices or evt.value is None:
                    raise EventProtocolError(f"OVERWRITE требует данных на шаге {idx}")
                mirror_data[evt.indices[0]] = evt.value

    @property
    def errors(self) -> list[str]:
        """Возвращает список накопленных ошибок валидации."""
        return self._errors.copy()
