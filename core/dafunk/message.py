from dataclasses import dataclass, field
from typing import Any, Optional, Union

import uuid
from orjson import orjson
from pydantic import BaseModel


@dataclass(frozen=True)
class Message:
    payload: Any
    headers: Optional[dict[str, Union[str, int, float]]] = field(default_factory=dict)
    id: Optional[uuid.UUID] = field(default_factory=lambda: str(uuid.uuid4()))


    def get_bites(self) -> bytes:
        if issubclass(type(self.payload), BaseModel):
            payload = self.payload.model_dump()
        else:
            payload = self.payload
        data_json = orjson.dumps(
            {
                "id": self.id,
                "payload": payload,
            }
        )
        if bool(self.headers):
            data_json['headers'] = self.headers

        return data_json

