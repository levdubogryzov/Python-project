from typing import List, Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType


class QuickSort(BaseAlgorithm):
    """Быстрая сортировка с событиями для визуализации."""

    def __init__(self, data: List[int]) -> None:
        super().__init__(data)

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        if len(self._data) > 0:
            yield from self._quick_sort(0, len(self._data) - 1)

    def _quick_sort(self, low: int, high: int) -> Generator[AlgorithmEvent, None, None]:
        if low < high:
            pi = yield from self._partition(low, high)
            if pi is not None:
                yield from self._quick_sort(low, pi - 1)
                yield from self._quick_sort(pi + 1, high)

    def _partition(self, low: int, high: int) -> Generator[AlgorithmEvent, None, int]:
        pivot = self._data[high]
        i = low - 1

        yield self._emit(
            EventType.PARTITION,
            [low, high],
            pivot,
            f"Разделение диапазона [{low}, {high}]"
        )

        for j in range(low, high):
            yield self._emit(
                EventType.COMPARE,
                [j, high],
                self._data[j],
                f"Сравнение [{j}]={self._data[j]} с опорным {pivot}"
            )

            if self._data[j] <= pivot:
                i += 1
                if i != j:
                    self._data[i], self._data[j] = self._data[j], self._data[i]
                    yield self._emit(
                        EventType.SWAP,
                        [i, j],
                        None,
                        f"Обмен [{i}] и [{j}]"
                    )

        if i + 1 != high:
            self._data[i + 1], self._data[high] = self._data[high], self._data[i + 1]
            yield self._emit(
                EventType.SWAP,
                [i + 1, high],
                None,
                "Финальная установка опорного элемента"
            )

        return i + 1
