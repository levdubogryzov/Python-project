from __future__ import annotations
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from src.core.events import EventType, AlgorithmEvent


class EventRecord(BaseModel):
    """Модель события для хранения и передачи в формате JSON."""

    model_config = ConfigDict(extra="ignore", from_attributes=True)

    step_id: int = Field(..., ge=0)
    event_type: EventType
    indices: List[int] = Field(default_factory=list)
    value: Optional[Any] = None
    description: str = ""
    timestamp: float = Field(default=0.0, ge=0.0)

    def to_event(self) -> AlgorithmEvent:
        """Конвертирует запись в объект AlgorithmEvent."""
        return AlgorithmEvent(
            event_type=self.event_type,
            indices=self.indices,
            value=self.value,
            description=self.description,
            timestamp=self.timestamp,
        )
