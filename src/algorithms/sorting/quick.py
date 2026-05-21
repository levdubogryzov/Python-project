from __future__ import annotations
from typing import List, Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType


class QuickSort(BaseAlgorithm):
    """Быстрая сортировка с использованием схемы Хоара/Ломуто и генерацией событий."""
    def __init__(self, data: List[int]) -> None:
        super().__init__(data)

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Запускает рекурсивный процесс сортировки и генерирует финальное событие завершения."""
        if len(self._data) > 0:
            yield from self._quick_sort(0, len(self._data) - 1)
            yield self._emit(
                event_type=EventType.VISIT,
                indices=list(range(len(self._data))),
                description="Сортировка завершена"
            )

    def _quick_sort(self, low: int, high: int) -> Generator[AlgorithmEvent, None, None]:
        """Рекурсивно разделяет массив и вызывает сортировку для подмассивов."""
        if low < high:
            pi = yield from self._partition(low, high)
            if pi is not None:
                yield from self._quick_sort(low, pi - 1)
                yield from self._quick_sort(pi + 1, high)

    def _partition(self, low: int, high: int) -> Generator[AlgorithmEvent, None, int]:
        """Разбивает массив относительно опорного элемента и генерирует события сравнения/обмена."""
        pivot = self._data[high]
        i = low - 1

        yield self._emit(
            event_type=EventType.PIVOT,
            indices=[high],
            value=float(pivot),
            description=f"Опорный элемент: {pivot}"
        )

        for j in range(low, high):
            yield self._emit(
                event_type=EventType.COMPARE,
                indices=[j, high],
                description=f"Сравнение {self._data[j]} с {pivot}"
            )

            if self._data[j] <= pivot:
                i += 1
                if i != j:
                    self._data[i], self._data[j] = self._data[j], self._data[i]
                    yield self._emit(
                        event_type=EventType.SWAP,
                        indices=[i, j],
                        description=f"Обмен {self._data[i]} и {self._data[j]}"
                    )

        pivot_idx = i + 1
        if pivot_idx != high:
            self._data[pivot_idx], self._data[high] = self._data[high], self._data[pivot_idx]
            yield self._emit(
                event_type=EventType.SWAP,
                indices=[pivot_idx, high],
                description=f"Установка опорного {pivot}"
            )

        yield self._emit(
            event_type=EventType.VISIT,
            indices=[pivot_idx],
            description=f"Элемент {pivot} зафиксирован"
        )

        return pivot_idx
