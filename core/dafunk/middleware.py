import json
from typing import Optional, Any, Callable, Awaitable

from aiokafka import ConsumerRecord
from faststream import BaseMiddleware

from core.dafunk import DaEvent


class DaBrokerMiddleware(BaseMiddleware):

    def __init__(self, msg: Optional[Any] = None,
                 *,
                 settings: dict) -> None:
        self._settings = settings
        self._hashmap = None
        super().__init__(msg)


    async def on_receive(self) -> None:
        data = self._to_dict()
        if "hashmap" in data:
            self._hashmap = data["hashmap"]
            print("Received: ", data['hashmap'])
        return await super().on_receive()

    def _to_dict(self, msg = None) -> dict:
        if msg is None:
            msg = self.msg
        if isinstance(msg, ConsumerRecord):
            data = msg.value.decode()
            json_data = json.loads(data)
            return json_data
        elif isinstance(msg, DaEvent):
            return msg.model_dump()
        return {}

    def _check_service_name(self, service_name: str) -> bool:
        if self._settings['name'] == service_name:
            return True
        return False

    async def publish_scope(
        self,
        call_next: Callable[..., Awaitable[Any]],
        msg: Any,
        **options: Any,
    ) -> Any:
        if self._hashmap is not None:
            data = self._to_dict(msg)
            print("Published dict: ", data)
            self._hashmap = None
        return await call_next(msg, **options)

class BaseDaBrokerMiddleware:
    __slots__ = "_settings"

    def __init__(self, settings: dict):
        self._settings = settings

    def __call__(self, msg: Optional[Any]):
        return DaBrokerMiddleware(msg=msg,settings=self._settings)
