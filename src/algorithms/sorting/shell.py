from typing import Generator
from src.algorithms.base import BaseAlgorithm
from src.core.events import AlgorithmEvent, EventType


class ShellSort(BaseAlgorithm):
    """Сортировка Шелла с генерацией событий сравнения и перезаписи для визуализации."""
    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Выполняет сортировку, пошагово генерируя события для каждого сравнения и сдвига элементов."""
        n = len(self._data)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = self._data[i]
                j = i
                while j >= gap:
                    yield self._emit(
                        event_type=EventType.COMPARE,
                        indices=[j - gap, j],
                        description=f"Сравнение {j - gap} и {j}"
                    )
                    if self._data[j - gap] <= temp:
                        break

                    self._data[j] = self._data[j - gap]
                    yield self._emit(
                        event_type=EventType.OVERWRITE,
                        indices=[j],
                        value=float(self._data[j]),
                        description=f"Сдвиг на {j}"
                    )
                    j -= gap

                self._data[j] = temp
                yield self._emit(
                    event_type=EventType.OVERWRITE,
                    indices=[j],
                    value=float(temp),
                    description=f"Вставка на {j}"
                )
            gap //= 2
