from abc import ABC, abstractmethod
from typing import Generator, List, Any, Optional, Dict
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import InvalidInputError


class BaseAlgorithm(ABC):
    """Абстрактный базовый класс, определяющий интерфейс для всех алгоритмов визуализации."""

    def __init__(self, data: List[Any]) -> None:
        """Инициализирует базовое состояние и выполняет валидацию входных данных."""
        self._validate_input(data)
        self._data = list(data)
        self._steps_count = 0

    @property
    def data(self) -> List[Any]:
        """Возвращает текущую копию структуры данных алгоритма."""
        return self._data.copy()

    def _emit(
        self,
        event_type: EventType,
        indices: List[int],
        value: Optional[Any] = None,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None
    ) -> AlgorithmEvent:
        """Создает и возвращает объект события, увеличивая счетчик шагов."""
        self._steps_count += 1
        return AlgorithmEvent(
            event_type=event_type,
            indices=indices,
            value=value,
            description=description,
            metadata=metadata or {}
        )

    @abstractmethod
    def run(self) -> Generator[AlgorithmEvent, None, None]:
        """Основной метод алгоритма, генерирующий поток событий."""
        pass

    @staticmethod
    def _validate_input(data: List[Any]) -> None:
        """Проверяет корректность входного списка данных."""
        if not isinstance(data, list) or not data:
            raise InvalidInputError("Данные должны быть непустым списком.")
