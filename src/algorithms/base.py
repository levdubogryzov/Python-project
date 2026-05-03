from abc import ABC, abstractmethod
from typing import Generator, List, Any, Optional

from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError


class BaseAlgorithm(ABC):
    """Абстрактный базовый класс для всех алгоритмов."""

    def __init__(self,  data: List[Any]) -> None:
        self._validate_input(data)
        self._data = list(data)
        self._steps_count = 0

    @property
    def data(self) -> List[Any]:
        """Текущее состояние данных (копия)."""
        return self._data.copy()

    @property
    def steps_count(self) -> int:
        """Количество выполненных шагов."""
        return self._steps_count

    def _emit(
        self,
        event_type: EventType,
        indices: List[int],
        value: Optional[Any] = None,
        description: str = "",
    ) -> AlgorithmEvent:
        """Создаёт событие и автоматически увеличивает счётчик шагов."""
        self._steps_count += 1
        return AlgorithmEvent(
            event_type=event_type,
            indices=indices,
            value=value,
            description=description,
        )

    @abstractmethod
    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Запускает алгоритм и генерирует поток событий."""
        pass

    @classmethod
    def from_string(cls, data_str: str, separator: str = ",") -> "BaseAlgorithm":
        """Создаёт экземпляр алгоритма из строки."""
        try:
            parsed = [int(x.strip()) for x in data_str.split(separator)]
            return cls(parsed)
        except ValueError as exc:
            raise InvalidInputError("Неверный формат строки.") from exc

    @staticmethod
    def _validate_input(data: List[Any]) -> None:
        """Проверяет корректность входных данных."""
        if not isinstance(data, list):
            raise InvalidInputError("Данные должны быть списком.")
        if not len(data) > 0:
            raise InvalidInputError("Список не может быть пустым.")
