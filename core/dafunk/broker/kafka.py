import asyncio

from loguru._logger import Logger

from core.dafunk.broker import DaBrokerConsumer
from core.dafunk.settings import BrokerSettings


class DaKafkaBroker:
    __slots__ = ("_topics", "_message", "_settings", "_consumer", "_logger")
    def __init__(self, settings: BrokerSettings, logger: Logger) -> None:
        self._settings = settings
        self._logger = logger
        self._message = None
        self._consumer = None

    async def start(self, topics: list[str],
              queue: asyncio.Queue) -> None:
        self._logger.info("Start Kafka Consumer Broker.")
        consumer = DaBrokerConsumer(self._settings, topics, self._logger)
        await consumer.start(queue)






