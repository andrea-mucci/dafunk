from dataclasses import dataclass
from typing import Any

from orjson import orjson
from pydantic import BaseModel


@dataclass(frozen=True)
class Message:
    uuid: str
    payload: Any


    def get_bites(self) -> bytes:
        if isinstance(self.payload, BaseModel):
            payload = self.payload.model_dump()
        else:
            payload = self.payload
        data_json = orjson.dumps(
            {
                "uuid": self.uuid,
                "payload": payload,
            }
        )
        return data_json

