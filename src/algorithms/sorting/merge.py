from typing import Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType


class MergeSort(BaseAlgorithm):
    """Сортировка слиянием с генерацией событий для визуализации."""

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Запускает процесс сортировки слиянием."""
        if self._data:
            yield from self._merge_sort(0, len(self._data) - 1)

    def _merge_sort(self, left: int, right: int) -> Generator[AlgorithmEvent, None, None]:
        """Рекурсивно разделяет массив и запускает слияние."""
        if left < right:
            mid = (left + right) // 2

            yield self._emit(
                event_type=EventType.SPLIT,
                indices=[left, mid, right],
                description=f"Разделение диапазона на [{left}:{mid}] и [{mid + 1}:{right}]"
            )

            yield from self._merge_sort(left, mid)
            yield from self._merge_sort(mid + 1, right)
            yield from self._merge(left, mid, right)

    def _merge(self, left: int, mid: int, right: int) -> Generator[AlgorithmEvent, None, None]:
        """Сливает два отсортированных подмассива в один."""
        left_arr = self._data[left: mid + 1]
        right_arr = self._data[mid + 1: right + 1]

        i = j = 0
        k = left

        while i < len(left_arr) and j < len(right_arr):
            yield self._emit(
                event_type=EventType.COMPARE,
                indices=[left + i, mid + 1 + j],
                description=f"Сравнение элементов {left_arr[i]} и {right_arr[j]}"
            )

            if left_arr[i] <= right_arr[j]:
                self._data[k] = left_arr[i]
                yield self._emit(
                    event_type=EventType.OVERWRITE,
                    indices=[k],
                    value=left_arr[i],
                    description=f"Запись значения {left_arr[i]} в позицию {k}"
                )
                i += 1
            else:
                self._data[k] = right_arr[j]
                yield self._emit(
                    event_type=EventType.OVERWRITE,
                    indices=[k],
                    value=right_arr[j],
                    description=f"Запись значения {right_arr[j]} в позицию {k}"
                )
                j += 1
            k += 1

        while i < len(left_arr):
            self._data[k] = left_arr[i]
            yield self._emit(
                event_type=EventType.OVERWRITE,
                indices=[k],
                value=left_arr[i],
                description=f"Перенос остатка {left_arr[i]} в позицию {k}"
            )
            i += 1
            k += 1

        while j < len(right_arr):
            self._data[k] = right_arr[j]
            yield self._emit(
                event_type=EventType.OVERWRITE,
                indices=[k],
                value=right_arr[j],
                description=f"Перенос остатка {right_arr[j]} в позицию {k}"
            )
            j += 1
            k += 1
