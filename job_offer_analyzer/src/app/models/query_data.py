from pydantic import BaseModel
from typing import Optional
from enum import Enum, auto


class JobType(Enum):
    part_time: auto()
    full_time: auto()


class QueryData(BaseModel):
    query: str
    location: Optional[str]
    job_type: JobType
