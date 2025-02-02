import functools
from typing import Any

from anyio import create_task_group, create_memory_object_stream


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


    async def start(self, events_processes: bool = True, web_processes: bool = False, websockets_processes: bool = False):
        send_event_stream, receive_event_stream = create_memory_object_stream[dict[str, Any]]()
        async with create_task_group() as tg:
            if events_processes:
                consumer = DaKafkaBroker(self._settings.broker)
                consumer.start(list(self._events_routes.keys()),
                               send_event_stream,
                               tg)
                async with receive_event_stream:
                    async for item in receive_event_stream:
                        print('received', item)
