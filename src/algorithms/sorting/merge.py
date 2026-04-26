from typing import Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import EventType, AlgorithmEvent


class MergeSort(BaseAlgorithm):
    """Сортировка слиянием с генерацией событий."""

    _is_completed: bool

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        yield from self._sort(0, len(self._data) - 1)
        self._is_completed = True
        yield self._emit(EventType.STATE_CHANGE, tuple(range(len(self._data))), tuple(self._data), status="sorted")

    def _sort(self, left: int, right: int) -> Generator[AlgorithmEvent, None, None]:
        if left < right:
            mid = (left + right) // 2
            yield from self._sort(left, mid)
            yield from self._sort(mid + 1, right)
            yield from self._merge(left, mid, right)

    def _merge(self, left: int, mid: int, right: int) -> Generator[AlgorithmEvent, None, None]:
        left_arr = self._data[left:mid + 1]
        right_arr = self._data[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_arr) and j < len(right_arr):
            yield self._emit(EventType.COMPARE, (left + i, mid + 1 + j), (left_arr[i], right_arr[j]))
            if left_arr[i] <= right_arr[j]:
                self._data[k] = left_arr[i]
                yield self._emit(EventType.OVERWRITE, (k,), (left_arr[i],))
                i += 1
            else:
                self._data[k] = right_arr[j]
                yield self._emit(EventType.OVERWRITE, (k,), (right_arr[j],))
                j += 1
            k += 1
        while i < len(left_arr):
            self._data[k] = left_arr[i]
            yield self._emit(EventType.OVERWRITE, (k,), (left_arr[i],))
            i += 1
            k += 1
        while j < len(right_arr):
            self._data[k] = right_arr[j]
            yield self._emit(EventType.OVERWRITE, (k,), (right_arr[j],))
            j += 1
            k += 1
