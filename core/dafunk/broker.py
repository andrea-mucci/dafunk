from core.dafunk.settings import DaSettings


class DaKafkaBroker:
    __slots__ = ("broker_url", "_topics", "_message", )
    def __init__(self, settings: DaSettings) -> None:
        configs = {'bootstrap.servers': settings.broker.url}
        self._topics = []
        self._message = None


    def set_consumer_topics(self, topics: list[str]):
        if isinstance(topics, list):
            self._topics = topics




