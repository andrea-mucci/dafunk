import sys

from confluent_kafka import Consumer

from core.dafunk.exceptions import BrokerConsumerException
from core.dafunk.settings import DaSettings


class DaKafkaBroker:
    __slots__ = ("_topics", "_message", "_configs", "_consumer")
    def __init__(self, settings: DaSettings) -> None:
        self._configs = {
            'bootstrap.servers': settings.broker.url,
            'group.id': settings.broker.group,
            'session.timeout.ms': settings.broker.session_timeout,
            'auto.offset.reset': settings.broker.offset_reset,
            'enable.auto.offset.store': settings.broker.auto_offset,}
        self._topics = []
        self._message = None
        self._consumer = None


    def set_consumer_topics(self, topics: list[str]):
        if isinstance(topics, list):
            self._topics = topics

    def set_consumer(self):
        if self._consumer is None:
            self._consumer = Consumer(self._configs)
            self._consumer.subscribe(self._topics)

    async def start_consumer(self):
        if self._consumer is not None:
            try:
                while True:
                    msg = await self._consumer.poll(timeout=1.0)
                    if msg is None:
                        continue
                    elif msg.error():
                        raise BrokerConsumerException(msg.error())
                    else:
                        topic = msg.topic()
            except KeyboardInterrupt:
                sys.stderr.write("Aborted By User")
            finally:
                self._consumer.close()





