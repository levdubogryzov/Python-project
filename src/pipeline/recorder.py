from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Iterator, Any
from src.core.events import AlgorithmEvent


class EventRecorder:
    """Класс для записи потока событий алгоритма в JSON-файл для последующей визуализации."""
    def __init__(self, output_path: Path | str) -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def record(
            self,
            events: Iterator[AlgorithmEvent],
            algorithm_name: str = "Unknown",
            initial_state: Any = None
    ) -> Path:
        """Потребляет генератор событий, обогащает их метаданными и сохраняет на диск."""
        records = []

        try:
            for step_id, event in enumerate(events):
                record_dict = {
                    "step_id": step_id,
                    "event_type": event.type.value,
                    "indices": event.indices,
                    "value": event.value,
                    "description": event.description,
                    "timestamp": time.time()
                }
                records.append(record_dict)
        except Exception as e:
            print(f"Ошибка при записи шага {len(records)}: {e}")

        output_data = {
            "algorithm": algorithm_name,
            "initial_state": initial_state,
            "events": records,
            "total_steps": len(records)
        }

        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(output_data, file, indent=2, ensure_ascii=False)

        return self.output_path
