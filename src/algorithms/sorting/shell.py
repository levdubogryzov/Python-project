from typing import Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import EventType, AlgorithmEvent


class ShellSort(BaseAlgorithm):
    """Сортировка Шелла с генерацией событий."""

    _is_completed: bool

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        n = len(self._data)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = self._data[i]
                yield self._emit(EventType.ACCESS, (i,), (temp,))

                j = i
                while j >= gap and self._data[j - gap] > temp:
                    yield self._emit(EventType.COMPARE, (j, j - gap), (self._data[j], self._data[j - gap]))
                    self._data[j] = self._data[j - gap]
                    yield self._emit(EventType.SWAP, (j, j - gap), (self._data[j - gap], temp))
                    j -= gap

                self._data[j] = temp
            gap //= 2
        self._is_completed = True
        yield self._emit(EventType.STATE_CHANGE, tuple(range(n)), tuple(self._data), status="sorted")
