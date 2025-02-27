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

class HttpServerException(Exception):
    pass

class EventMethodError(Exception):
    pass

class ServiceException(Exception):
    pass
