from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict

Status = Literal["planned", "in_progress", "done"]

class TopicBase(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    description: Optional[str] = None
    status: Status = "planned"

class TopicCreate(TopicBase):
    pass

class TopicUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=128)
    description: Optional[str] = None
    status: Optional[Status] = None

class Topic(TopicBase):
    id: int
    # для pydantic v2 — читаем из ORM-объектов
    model_config = ConfigDict(from_attributes=True)
