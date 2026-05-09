"""Модуль пошагового воспроизведения событий из JSON-лога."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Iterator

from src.core.events import AlgorithmEvent
from src.pipeline.schemas import EventRecord


class EventPlayer:
    """Воспроизводит записанные события с настраиваемой задержкой."""

    def __init__(self, file_path: Path | str) -> None:
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"Файл событий не найден: {self.file_path}")

    def play(self, delay: float = 0.0, limit: int | None = None) -> Iterator[AlgorithmEvent]:
        """Генерирует события из файла с опциональной задержкой и лимитом."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for index, item in enumerate(data):
            if limit is not None and index >= limit:
                break
            record = EventRecord.model_validate(item)
            if delay > 0:
                time.sleep(delay)
            yield record.to_event()
