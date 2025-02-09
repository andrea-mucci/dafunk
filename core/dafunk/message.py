from dataclasses import dataclass, field
from typing import Any

from orjson import orjson


@dataclass(frozen=True)
class DaMessage:
    uuid: str
    payload: Any


    def get_bites(self) -> bytes:
        data_json = orjson.dumps(
            {
                "uuid": self.uuid,
                "payload": self.payload
            }
        )
        return data_json

