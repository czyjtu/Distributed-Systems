from pydantic import BaseModel
from typing import Optional
from enum import Enum, auto


class JobType(Enum):
    PART_TIME = auto()
    FULL_TIME = auto()


class QueryData(BaseModel):
    query: str
    location: str
    job_type: JobType
