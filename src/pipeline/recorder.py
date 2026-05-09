"""Модуль записи потока событий алгоритма в JSON-файл."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Iterator

from src.core.events import AlgorithmEvent
from src.pipeline.schemas import EventRecord


class EventRecorder:
    """Записывает итерируемый поток событий в JSON с разметкой шагов."""

    def __init__(self, output_path: Path | str) -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, events: Iterator[AlgorithmEvent]) -> Path:
        """Сохраняет поток событий в файл формата JSON."""
        with open(self.output_path, "w", encoding="utf-8") as file:
            file.write("[\n")
            first = True
            for step_id, event in enumerate(events):
                if event.timestamp <= 0:
                    event.timestamp = time.time()

                record = EventRecord(
                    step_id=step_id,
                    event_type=event.event_type,
                    indices=event.indices,
                    value=event.value,
                    description=event.description,
                    timestamp=event.timestamp,
                )
                if not first:
                    file.write(",\n")
                file.write("  " + record.model_dump_json(indent=2))
                first = False
            file.write("\n]")
        return self.output_path
