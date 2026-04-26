from typing import Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import EventType, AlgorithmEvent


class QuickSort(BaseAlgorithm):
    """Быстрая сортировка с генерацией событий."""

    _is_completed: bool

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        yield from self._sort(0, len(self._data) - 1)
        self._is_completed = True
        yield self._emit(EventType.STATE_CHANGE, tuple(range(len(self._data))), tuple(self._data), status="sorted")

    def _sort(self, low: int, high: int) -> Generator[AlgorithmEvent, None, None]:
        if low < high:
            pi = yield from self._partition(low, high)
            yield from self._sort(low, pi - 1)
            yield from self._sort(pi + 1, high)

    def _partition(self, low: int, high: int) -> Generator[AlgorithmEvent, None, int]:
        pivot = self._data[high]
        yield self._emit(EventType.ACCESS, (high,), (pivot,))
        i = low - 1
        for j in range(low, high):
            yield self._emit(EventType.COMPARE, (j, high), (self._data[j], pivot))
            if self._data[j] <= pivot:
                i += 1
                self._data[i], self._data[j] = self._data[j], self._data[i]
                yield self._emit(EventType.SWAP, (i, j), (self._data[i], self._data[j]))
        self._data[i + 1], self._data[high] = self._data[high], self._data[i + 1]
        yield self._emit(EventType.SWAP, (i + 1, high), (self._data[i + 1], self._data[high]))
        return i + 1
