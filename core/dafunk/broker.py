from faststream.kafka import KafkaBroker
from faststream.nats import NatsBroker

from core.dafunk.middleware import BaseDaBrokerMiddleware

class DaBroker(object):
    @classmethod
    def from_settings(cls, settings: dict) -> NatsBroker | KafkaBroker:
        broker_url = settings["broker_url"]
        if broker_url.startswith("nats://"):
            broker = NatsBroker(broker_url, middlewares=(
                BaseDaBrokerMiddleware(settings),
            ))
        else:
            broker = KafkaBroker(broker_url, middlewares=(
                BaseDaBrokerMiddleware(settings),
            ))
        return broker

