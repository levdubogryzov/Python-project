from typing import List, Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType


class ShellSort(BaseAlgorithm):
    """Сортировка Шелла с событиями для визуализации."""

    def __init__(self, data: List[int]) -> None:
        super().__init__(data)

    def run(self) -> Generator[AlgorithmEvent, None, None]:
        n = len(self._data)
        gap = n // 2

        while gap > 0:
            yield self._emit(
                event_type=EventType.STATE_CHANGE,
                indices=[],
                value=gap,
                description=f"Новый шаг (gap): {gap}",
            )

            for i in range(gap, n):
                temp = self._data[i]
                j = i

                yield self._emit(
                    event_type=EventType.ACCESS,
                    indices=[i],
                    value=temp,
                    description=f"Сохранён элемент [{i}] = {temp}",
                )

                while j >= gap and self._data[j - gap] > temp:
                    yield self._emit(
                        event_type=EventType.COMPARE,
                        indices=[j - gap, j],
                        value=None,
                        description=f"Сравнение [{j - gap}] = {self._data[j - gap]} > {temp}",
                    )

                    yield self._emit(
                        event_type=EventType.OVERWRITE,
                        indices=[j],
                        value=self._data[j - gap],
                        description=f"Сдвиг: [{j}] = [{j - gap}] = {self._data[j - gap]}",
                    )
                    self._data[j] = self._data[j - gap]
                    j -= gap

                if j != i:
                    yield self._emit(
                        event_type=EventType.OVERWRITE,
                        indices=[j],
                        value=temp,
                        description=f"Вставка: [{j}] = {temp}",
                    )
                    self._data[j] = temp

            gap //= 2
