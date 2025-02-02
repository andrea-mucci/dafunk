import asyncio
from asyncio import TaskGroup

from core.dafunk.broker import DaBrokerConsumer
from core.dafunk.settings import BrokerSettings


class DaKafkaBroker:
    __slots__ = ("_topics", "_message", "_settings", "_consumer")
    def __init__(self, settings: BrokerSettings) -> None:
        self._settings = settings

        self._message = None
        self._consumer = None

    async def start(self, topics: list[str],
              queue: asyncio.Queue) -> None:

        consumer = DaBrokerConsumer(self._settings, topics)
        await consumer.start(queue)






