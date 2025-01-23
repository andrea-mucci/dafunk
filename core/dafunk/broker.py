from typing import Type

from faststream.kafka import KafkaBroker
from faststream.nats import NatsBroker


class DaBroker(object):
    @classmethod
    def from_settings(cls, settings: dict) -> NatsBroker | KafkaBroker:
        broker_url = settings["broker_url"]
        if broker_url.startswith("nats://"):
            broker = NatsBroker(broker_url)
        else:
            broker = KafkaBroker(broker_url)
        return broker
