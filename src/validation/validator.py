from copy import deepcopy
from typing import List, Set, Dict, Tuple
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import EventProtocolError


class AlgorithmValidator:
    ALLOWED_SORTING_EVENTS: Set[EventType] = {
        EventType.COMPARE,
        EventType.SWAP,
        EventType.ACCESS,
        EventType.OVERWRITE,
        EventType.STATE_CHANGE,
        EventType.PARTITION,
        EventType.MERGE,
        EventType.SPLIT,
    }

    ALLOWED_GRAPH_EVENTS: Set[EventType] = {
        EventType.VISIT,
        EventType.UPDATE,
        EventType.RELAX,
        EventType.HEURISTIC,
        EventType.NEGATIVE_CYCLE,
        EventType.FOUND,
    }

    def __init__(self) -> None:
        self._errors: List[str] = []

    def validate_sorting(
            self,
            events: List[AlgorithmEvent],
            initial_data: List[int],
    ) -> bool:
        self._errors.clear()
        mirror_data = deepcopy(initial_data)

        try:
            self._validate_events(events, self.ALLOWED_SORTING_EVENTS, mirror_data)
        except EventProtocolError as exc:
            self._errors.append(str(exc))
            return False
        except IndexError as exc:
            self._errors.append(f"Ошибка индекса при воспроизведении: {exc}")
            return False

        if not self._is_sorted(mirror_data):
            self._errors.append("Конечные данные не отсортированы.")
            return False

        return True

    def validate_graph(
            self,
            distances: Dict[int, float],
            graph: List[List[Tuple[int, float]]],
            start: int,
    ) -> bool:
        self._errors.clear()
        num_vertices = len(graph)

        if not isinstance(distances, dict):
            self._errors.append("Расстояния должны быть словарем.")
            return False

        if start < 0 or start >= num_vertices:
            self._errors.append(f"Некорректная стартовая вершина: {start}")
            return False

        if len(distances) != num_vertices:
            self._errors.append(
                f"Количество расстояний ({len(distances)}) не совпадает с числом вершин ({num_vertices})."
            )
            return False

        if distances.get(start, float('inf')) != 0:
            self._errors.append("Расстояние до стартовой вершины должно быть 0.")
            return False

        for vertex, dist in distances.items():
            if not isinstance(vertex, int) or vertex < 0 or vertex >= num_vertices:
                self._errors.append(f"Некорректный индекс вершины: {vertex}")
                return False

        for u in range(num_vertices):
            u_dist = distances.get(u, float('inf'))
            if u_dist == float('inf'):
                continue

            for v, weight in graph[u]:
                v_dist = distances.get(v, float('inf'))

                if v_dist != float('inf') and v_dist != float('-inf'):
                    if v_dist > u_dist + weight + 1e-9:
                        self._errors.append(
                            f"Нарушение оптимальности"
                        )
                        return False

        return True

    @staticmethod
    def _is_sorted(data: List[int]) -> bool:
        return all(
            data[i] <= data[i + 1]
            for i in range(len(data) - 1)
        )

    @staticmethod
    def _validate_events(
            events: List[AlgorithmEvent],
            allowed: Set[EventType],
            mirror_data: List[int],
    ) -> None:
        for idx, evt in enumerate(events):
            if evt.event_type not in allowed:
                msg = f"Недопустимый тип события '{evt.event_type}' на шаге {idx}."
                raise EventProtocolError(msg)

            if evt.indices:
                for i in evt.indices:
                    if not isinstance(i, int) or i < 0 or i >= len(mirror_data):
                        raise IndexError(f"Неверный индекс {i} в событии {evt.event_type} на шаге {idx}")

            if evt.event_type == EventType.SWAP:
                if len(evt.indices) != 2:
                    raise EventProtocolError(f"SWAP требует ровно 2 индекса на шаге {idx}")
                i, j = evt.indices
                mirror_data[i], mirror_data[j] = mirror_data[j], mirror_data[i]

            elif evt.event_type == EventType.OVERWRITE:
                if not evt.indices or evt.value is None:
                    raise EventProtocolError(f"OVERWRITE требует indices и value на шаге {idx}")
                target_idx = evt.indices[0]
                mirror_data[target_idx] = evt.value

    @property
    def errors(self) -> List[str]:
        return self._errors.copy()
