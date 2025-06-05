from enum import Enum
from uuid import uuid4
from typing import List, Literal
from pydantic import BaseModel

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class IngestionRequest(BaseModel):
    ids: List[int]
    priority: Priority

class BatchStatus(str, Enum):
    YET_TO_START = "yet_to_start"
    TRIGGERED = "triggered"
    COMPLETED = "completed"

class Batch:
    def __init__(self, ids: List[int]):
        self.batch_id = str(uuid4())
        self.ids = ids
        self.status = BatchStatus.YET_TO_START
