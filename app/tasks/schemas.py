# STDLIB
from typing import Literal, Optional

# THIRDPARTY
from pydantic import UUID4, BaseModel, Field


class STasks(BaseModel):
    uuid: UUID4
    user_id: UUID4
    name: str
    description: Optional[str]
    status: str


class SAddTasks(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    description: Optional[str] = Field(default=None, max_length=1000)


class SUpdateTasks(BaseModel):
    task_id: str
    status: Literal["WORKING", "COMPLETED"]
