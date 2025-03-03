import sys
from confluent_kafka import Producer, Consumer
from loguru._logger import Logger
from orjson import orjson

from core.dafunk import Message, BrokerConsumerException
from core.dafunk.broker import AdminBroker
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

class KafkaBroker:
    __slots__ = ("_topics", "_message", "_settings", "_consumer", "_logger")
    def __init__(self, settings: BrokerSettings, logger: Logger) -> None:
        self._settings = settings
        self._logger = logger
        self._message = None
        self._consumer = None
        self._topics = None

    def _create_topics(self) -> None:
        self._logger.debug('Creating topics: {}', self._topics)
        AdminBroker.create_topics(self._settings, self._topics)

    def _set_consumer_broker(self) -> Consumer:
        config = {
            'bootstrap.servers': self._settings.url,
            'group.id': self._settings.group,
            'session.timeout.ms': self._settings.session_timeout,
            'auto.offset.reset': self._settings.offset_reset,
            'enable.auto.offset.store': self._settings.auto_offset
        }
        self._logger.trace("Consumer Configuration: {}", config)
        self._logger.debug('Consumer Instance')
        return Consumer(config)

    @classmethod
    def producer(cls, topic: str, message: Message,
                 settings: BrokerSettings) -> None:
        producer_settings = {
            'bootstrap.servers': settings.url
        }
        p = Producer(producer_settings)
        p.poll(0.0)
        p.produce(topic, message.get_bites(), callback=callback_message)
        p.flush(10)

    def start(self, routes: dict) -> None:
        self._logger.info("Start Kafka Consumer Broker.")
        self._topics = list(routes.keys())
        self._logger.debug("Creating topics: {}", self._topics)
        self._create_topics()
        broker = self._set_consumer_broker()
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
                    self._logger.trace('Message Received with Topic: {topic} and Value: {value}',
                                       topic=msg.topic(), value=msg.value().decode('utf-8'))
                    self._logger.debug('Message Received With Topic: {}', msg.topic())
                    topic = msg.topic(),
                    content = msg.value().decode('utf-8')
                    if topic not in routes:
                        self._logger.trace("The topic does not exit: {}", topic)
                        pass
                    else:
                        self._logger.debug("The topic exit: {} and value {}", topic, content)
                        try:
                            funct = routes[topic]['func']
                            message_dict = orjson.loads(content)
                            if routes[topic]['model'] is not None:
                                model = routes[topic]['model']
                                message_data = model(**message_dict['payload'])
                            else:
                                message_data = message_dict['payload']
                            funct(message_data)
                        except Exception as e:
                            self._logger.error("Generic Error: {}".format(e))
                            raise BrokerConsumerException("The route returned a generic error: {}".format(e))
        except KeyboardInterrupt:
            self._logger.error('Received KeyboardInterrupt')
            sys.stderr.write("Aborted By User")
        finally:
            self._logger.debug('Closing Consumer')
            broker.close()
