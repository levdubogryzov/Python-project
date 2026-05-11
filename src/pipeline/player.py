from __future__ import annotations
import json
from pathlib import Path
from typing import Iterator
from src.core.events import AlgorithmEvent


class EventPlayer:
    """Класс для последовательного чтения событий из записанного лога."""

    def __init__(self, file_path: Path | str) -> None:
        """Инициализация игрока с проверкой существования файла лога."""
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл не найден: {self.file_path}")

    def fetch_events(self) -> Iterator[AlgorithmEvent]:
        """Итерирует по событиям из JSON, используя валидацию Pydantic."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data.get("events", []):
            yield AlgorithmEvent.model_validate(item)

    def play(self) -> Iterator[AlgorithmEvent]:
        """Алиас для совместимости со старыми вызовами в проекте."""
        return self.fetch_events()
