from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from core.dafunk.settings import BrokerSettings


class AdminBroker:
    __slots__ = ('_client', '_topics', '_num_partitions', '_replication_factor')
    def __init__(self, configs: BrokerSettings):
        self._replication_factor = configs.replication_factor
        self._num_partitions = configs.num_partitions
        self._client = AdminClient({
            'bootstrap.servers': configs.url,
        })

    @property
    def client(self) -> AdminClient:
        return self._client


    @classmethod
    def create_topics(cls, configs: BrokerSettings, topics: list[str]):
        class_admin_client = cls(configs)
        new_topics = [NewTopic(topic, num_partitions=configs.num_partitions,
                           replication_factor=configs.replication_factor)
                  for topic in topics]
        client = class_admin_client.client
        fs = client.create_topics(new_topics)
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))
