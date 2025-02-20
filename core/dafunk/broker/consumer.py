import asyncio
import sys

from confluent_kafka import Consumer
from loguru._logger import Logger

from core.dafunk import BrokerConsumerException
from core.dafunk.broker import AdminBroker
from core.dafunk.settings import BrokerSettings


class BrokerConsumer:
    __slots__ = ('_broker', '_topics', '_configs', '_logger')

    def __init__(self, configs: BrokerSettings, topics: list[str], logger: Logger):
        self._logger: Logger = logger
        self._configs = configs
        self._topics = topics

    def _create_topics(self) -> None:
        self._logger.debug('Creating topics: {}', self._topics)
        AdminBroker.create_topics(self._configs, self._topics)


    def _set_broker(self) -> Consumer:
        config = {
            'bootstrap.servers': self._configs.url,
            'group.id': self._configs.group,
            'session.timeout.ms': self._configs.session_timeout,
            'auto.offset.reset': self._configs.offset_reset,
            'enable.auto.offset.store': self._configs.auto_offset
        }
        self._logger.trace("Consumer Configuration: {}", config)
        self._logger.debug('Consumer Instance')
        return Consumer(config)


    async def start(self,
                    queue: asyncio.Queue
                    ):
        self._logger.info('Starting Consumer')
        self._create_topics()
        broker = self._set_broker()
        self._logger.debug('Connecting to Broker')
        broker.subscribe(self._topics)
        self._logger.trace('Starting While Loop for Consumer')
        try:
            while True:
                self._logger.trace('Consumer Poll')
                msg = broker.poll(timeout=1.0)
                if msg is None:
                    self._logger.trace('Message is None')
                    continue
                elif msg.error():
                    self._logger.critical('Consumer Error: {}', msg.error())
                    raise BrokerConsumerException(msg.error())
                else:
                    self._logger.trace('Message Received with Topic: {topic} and Value: {value}', topic=msg.topic(), value=msg.value().decode('utf-8'))
                    self._logger.debug('Message Received With Topic: {}', msg.topic())
                    await queue.put({
                        'topic': msg.topic(),
                        'content': msg.value().decode('utf-8')
                    })
                    await asyncio.sleep(0)
                    self._logger.trace('Consumer sent a None message to flush the queue')
                    await queue.put(None)

        except KeyboardInterrupt:
            self._logger.error('Received KeyboardInterrupt')
            sys.stderr.write("Aborted By User")
        finally:
            self._logger.debug('Closing Consumer')
            broker.close()



