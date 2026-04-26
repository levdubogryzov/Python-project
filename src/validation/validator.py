from typing import List, Set
from src.core.events import AlgorithmEvent, EventType
from src.core.exceptions import EventProtocolError


class AlgorithmValidator:
    """Валидатор потока событий и конечного состояния алгоритма."""

    ALLOWED_SORTING_EVENTS: Set[EventType] = {
        EventType.COMPARE,
        EventType.SWAP,
        EventType.ACCESS,
        EventType.OVERWRITE,
        EventType.STATE_CHANGE,
    }

    def __init__(self) -> None:
        self._errors: List[str] = []

    def validate_sorting(
        self,
        events: List[AlgorithmEvent],
        final_data: List[int],
    ) -> bool:
        """Проверяет корректность сортировки и валидность событий."""
        self._errors.clear()

        if not self._is_sorted(final_data):
            self._errors.append("Конечные данные не отсортированы.")
            return False

        try:
            self._validate_events(events, self.ALLOWED_SORTING_EVENTS)
        except EventProtocolError as exc:
            self._errors.append(str(exc))
            return False

        return True

    @staticmethod
    def _is_sorted(data: List[int]) -> bool:
        """Проверяет, отсортирован ли список по возрастанию."""
        return all(
            data[i] <= data[i + 1]
            for i in range(len(data) - 1)
        )

    @staticmethod
    def _validate_events(
        events: List[AlgorithmEvent],
        allowed: Set[EventType],
    ) -> None:
        """Проверяет типы событий на соответствие протоколу."""
        for idx, evt in enumerate(events):
            if evt.event_type not in allowed:
                msg = f"Недопустимый тип события '{evt.event_type}' на шаге {idx}."
                raise EventProtocolError(msg)

    @property
    def errors(self) -> List[str]:
        """Возвращает список накопленных ошибок (копию)."""
        return self._errors.copy()
