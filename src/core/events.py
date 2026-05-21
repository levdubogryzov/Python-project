from __future__ import annotations
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, ConfigDict


class EventType(Enum):
    COMPARE = "compare"
    SWAP = "swap"
    ACCESS = "access"
    OVERWRITE = "overwrite"
    STATE_CHANGE = "state_change"
    VISIT = "visit"
    UPDATE = "update"
    RELAX = "relax"
    HEURISTIC = "heuristic"
    NEGATIVE_CYCLE = "negative_cycle"
    FOUND = "found"
    PARTITION = "partition"
    MERGE = "merge"
    SPLIT = "split"
    PIVOT = "pivot"


class AlgorithmEvent(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: EventType = Field(alias="event_type")
    indices: list[int] = Field(default_factory=list)
    value: Any | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    description: str = ""

    def __repr__(self) -> str:
        return f"<{self.type.value.upper()} indices={self.indices}>"
