import asyncio
from typing import Union
from uuid import uuid4

from confluent_kafka import Producer
from loguru._logger import Logger
from orjson import orjson

from core.dafunk import DaMessage
from core.dafunk.broker import DaBrokerConsumer
from core.dafunk.settings import BrokerSettings


def callback_message(err, msg):
    if err is not None:
        print("Error: {}, {}".format(msg.key(), err))
        return
    print("Sent msg: Key: {}, Topic: {}, Partition: {}, Offset: {}".format(
        msg.key(),
        msg.topic(),
        msg.partition(),
        msg.offset()))

class DaKafkaBroker:
    __slots__ = ("_topics", "_message", "_settings", "_consumer", "_logger")
    def __init__(self, settings: BrokerSettings, logger: Logger) -> None:
        self._settings = settings
        self._logger = logger
        self._message = None
        self._consumer = None


    @classmethod
    def producer(cls, topic: str, message: Union[str, int, float, dict, list],
                 settings: BrokerSettings, logger: Logger) -> None:
        producer_settings = {
            'bootstrap.servers': settings.url

        }
        p = Producer(producer_settings)

        # Prepare Message Structure
        message_dataclass = DaMessage(
            uuid=uuid4().hex,
            payload = message
        )
        p.poll(0.0)
        p.produce(topic, message_dataclass.get_bites(), callback=callback_message)
        p.flush(10)

    async def start(self, topics: list[str],
              queue: asyncio.Queue) -> None:
        self._logger.info("Start Kafka Consumer Broker.")
        consumer = DaBrokerConsumer(self._settings, topics, self._logger)
        await consumer.start(queue)






