from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Protocol, Tuple


class EventType(Enum):
    """Перечисление типов алгоритмических событий."""
    COMPARE = auto()
    SWAP = auto()
    ACCESS = auto()
    OVERWRITE = auto()
    STATE_CHANGE = auto()
    NODE_VISITED = auto()
    PATH_UPDATED = auto()


@dataclass(frozen=True)
class AlgorithmEvent:
    """Атомарное событие алгоритма."""
    event_type: EventType
    indices: Tuple[int, ...]
    values: Tuple[Any, ...]
    metadata: dict[str, Any] = field(default_factory=dict)


class EventEmitterProtocol(Protocol):
    """Протокол для объектов, способных эмиттить события."""
    def emit(self, event: AlgorithmEvent) -> None: ...
