import uuid
from typing import Optional

from pydantic import BaseModel, Field


class DaEvent(BaseModel):
    name: Optional[str] = ""
    hashmap: str = Field(default_factory=lambda: str(uuid.uuid4()), frozen=True)
    partition: Optional[int] = 0
