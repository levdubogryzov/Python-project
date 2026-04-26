from abc import ABC, abstractmethod
from typing import Generator, List, Any, Tuple

from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError


class BaseAlgorithm(ABC):
    """Абстрактный базовый класс для алгоритмов."""

    _data: List[Any]
    _steps_count: int
    _is_completed: bool

    def __init__(self, data: List[Any]) -> None:
        self._validate_input(data)
        self._data = list(data)
        self._steps_count = 0
        self._is_completed = False

    @property
    def data(self) -> List[Any]:
        """Текущее состояние данных (копия)."""
        return self._data.copy()

    @property
    def steps_count(self) -> int:
        """Количество выполненных шагов."""
        return self._steps_count

    @property
    def is_completed(self) -> bool:
        """Флаг завершения алгоритма."""
        return self._is_completed

    def _emit(self, event_type: EventType, indices: Tuple[int, ...], values: Tuple[Any, ...],
              **kwargs: Any) -> AlgorithmEvent:
        self._steps_count += 1
        return AlgorithmEvent(event_type=event_type, indices=indices, values=values, metadata=kwargs)

    @abstractmethod
    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Запуск алгоритма и генерация событий."""
        pass

    @classmethod
    def from_string(cls, data_str: str, separator: str = ",") -> "BaseAlgorithm":
        try:
            parsed = [int(x.strip()) for x in data_str.split(separator)]
            return cls(parsed)
        except ValueError as e:
            raise InvalidInputError("Неверный формат строки.") from e

    @staticmethod
    def _validate_input(data: List[Any]) -> None:
        if not isinstance(data, list):
            raise InvalidInputError("Данные должны быть списком.")
        if not data:
            raise InvalidInputError("Список не может быть пустым.")
