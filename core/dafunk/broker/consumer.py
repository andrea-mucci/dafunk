import asyncio
import sys

from confluent_kafka import Consumer

from core.dafunk import BrokerConsumerException
from core.dafunk.broker import AdminBroker
from core.dafunk.settings import BrokerSettings


class DaBrokerConsumer:
    __slots__ = ('_broker', '_topics', '_configs')

    def __init__(self, configs: BrokerSettings, topics: list[str]):
        self._configs = configs
        self._topics = topics

    def _create_topics(self) -> None:
        AdminBroker.create_topics(self._configs, self._topics)


    def _set_broker(self) -> Consumer:
        config = {
            'bootstrap.servers': self._configs.url,
            'group.id': self._configs.group,
            'session.timeout.ms': self._configs.session_timeout,
            'auto.offset.reset': self._configs.offset_reset,
            'enable.auto.offset.store': self._configs.auto_offset
        }
        return Consumer(config)


    async def start(self,
                    queue: asyncio.Queue
                    ):
        self._create_topics()
        broker = self._set_broker()
        broker.subscribe(self._topics)

        try:
            while True:
                msg = broker.poll(timeout=1.0)
                if msg is None:
                    continue
                elif msg.error():
                    raise BrokerConsumerException(msg.error())
                else:
                    await queue.put({
                        'topic': msg.topic(),
                        'content': msg.value().decode('utf-8')
                    })
                    await asyncio.sleep(0)
                    print("message received")
                    await queue.put(None)
                    print("sent None to queue")
        except KeyboardInterrupt:
            sys.stderr.write("Aborted By User")
        finally:
            broker.close()



