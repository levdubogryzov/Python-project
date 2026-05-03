from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, List


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


@dataclass
class AlgorithmEvent:
    event_type: EventType
    indices: List[int]
    value: Optional[Any] = None
    description: str = ""
    timestamp: float = 0.0
