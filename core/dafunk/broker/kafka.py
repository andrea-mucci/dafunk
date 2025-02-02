from typing import Any

from anyio.abc import TaskGroup
from anyio.streams.memory import MemoryObjectSendStream

from core.dafunk.broker import DaBrokerConsumer
from core.dafunk.settings import BrokerSettings


class DaKafkaBroker:
    __slots__ = ("_topics", "_message", "_settings", "_consumer")
    def __init__(self, settings: BrokerSettings) -> None:
        self._settings = settings

        self._message = None
        self._consumer = None

    def start(self, topics: list[str],
              send_event_stream: MemoryObjectSendStream[dict[str, Any]],
              tg: TaskGroup) -> None:

        consumer = DaBrokerConsumer(self._settings, topics)
        tg.start_soon(consumer.start, send_event_stream)





