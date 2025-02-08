import asyncio
from typing import Union

from confluent_kafka import Producer
from loguru._logger import Logger
from orjson import orjson

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
        encode_message = b''
        if isinstance(message, str):
            encode_message = message.encode('utf-8')
        elif isinstance(message, int) or isinstance(message, float):
            encode_message = message
        elif isinstance(message, dict) or isinstance(message, list):
            encode_message = orjson.dumps(message)

        p.poll(0.0)
        p.produce(topic, encode_message, callback=callback_message)
        p.flush(10)

    async def start(self, topics: list[str],
              queue: asyncio.Queue) -> None:
        self._logger.info("Start Kafka Consumer Broker.")
        consumer = DaBrokerConsumer(self._settings, topics, self._logger)
        await consumer.start(queue)






