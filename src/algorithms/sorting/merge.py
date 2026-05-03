from typing import List, Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType


class MergeSort(BaseAlgorithm):
    """Сортировка слиянием с событиями для визуализации."""

    def __init__(self, data: List[int]) -> None:
        super().__init__(data)

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        if len(self._data) > 0:
            yield from self._merge_sort(0, len(self._data) - 1)

    def _merge_sort(self, left: int, right: int) -> Generator[AlgorithmEvent, None, None]:
        if left < right:
            mid = (left + right) // 2

            yield self._emit(
                EventType.SPLIT,
                [left, mid, right],
                description=f"Разделение: [{left}:{right}] -> [{left}:{mid}], [{mid + 1}:{right}]",
            )

            yield from self._merge_sort(left, mid)
            yield from self._merge_sort(mid + 1, right)
            yield from self._merge(left, mid, right)

    def _merge(self, left: int, mid: int, right: int) -> Generator[AlgorithmEvent, None, None]:
        left_arr = self._data[left: mid + 1]
        right_arr = self._data[mid + 1: right + 1]

        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            yield self._emit(
                EventType.COMPARE,
                [left + i, mid + 1 + j],
                description=f"Слияние: {left_arr[i]} vs {right_arr[j]}",
            )

            if left_arr[i] <= right_arr[j]:
                self._data[k] = left_arr[i]
                yield self._emit(
                    EventType.OVERWRITE,
                    [k],
                    value=left_arr[i],
                    description=f"Запись [{k}] = {left_arr[i]}",
                )
                i += 1
            else:
                self._data[k] = right_arr[j]
                yield self._emit(
                    EventType.OVERWRITE,
                    [k],
                    value=right_arr[j],
                    description=f"Запись [{k}] = {right_arr[j]}",
                )
                j += 1
            k += 1

        while i < len(left_arr):
            self._data[k] = left_arr[i]
            yield self._emit(
                EventType.OVERWRITE,
                [k],
                value=left_arr[i],
                description=f"Копирование остатка: [{k}] = {left_arr[i]}",
            )
            i += 1
            k += 1

        while j < len(right_arr):
            self._data[k] = right_arr[j]
            yield self._emit(
                EventType.OVERWRITE,
                [k],
                value=right_arr[j],
                description=f"Копирование остатка: [{k}] = {right_arr[j]}",
            )
            j += 1
            k += 1
