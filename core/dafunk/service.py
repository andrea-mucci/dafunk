import functools

from anyio import to_process

from core.dafunk import DaSettings, BrokerProtocolException
from core.dafunk.broker import DaKafkaBroker
from enum import Enum

class Protocol(Enum):
    WEB = 1
    WEBSOCKET = 2
    EVENT = 3

class DaService:
    __slots__ = ("_settings", "_broker", "_events_routes", "_web_routes", "_websockets_routes")

    def __init__(self, settings: DaSettings):
        self._settings = settings
        self._events_routes = {}
        self._web_routes = {}
        self._websockets_routes = {}

    @property
    def events_routes(self):
        return list(self._events_routes.keys())


    @property
    def web_routes(self):
        return list(
            self._web_routes.keys()
        )


    @property
    def websockets_routes(self):
        return list(
            self._websockets_routes.keys()
        )


    def _configure_broker(self):
        self._broker = DaKafkaBroker(settings=self._settings)
        self._broker.set_consumer_topics(
            list(
                self._events_routes.keys()
            )
        )

    def route(self, route: str, protocol: str = Protocol.EVENT):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            if protocol == Protocol.EVENT:
                self._events_routes[route] = func
            elif protocol == Protocol.WEB:
                self._web_routes[route] = func
            elif protocol == Protocol.WEBSOCKET:
                self._websockets_routes[route] = func
            else:
                raise BrokerProtocolException("Protocol not supported")
            return wrapper
        return decorator


    def start(self, events_processes: bool = True, web_processes: bool = False, websockets_processes: bool = False):
        if events_processes:
            self._configure_broker()

