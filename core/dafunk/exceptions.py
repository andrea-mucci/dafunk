class StorageUploadException(Exception):
    pass


class StorageDeleteException(Exception):
    pass

class BrokerException(Exception):
    pass

class BrokerProtocolException(BrokerException):
    pass

class BrokerConsumerException(BrokerException):
    pass
