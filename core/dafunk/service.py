import asyncio
import functools
import os
from typing import Any

from loguru import logger
from loguru._logger import Logger

from core.dafunk import DaSettings, BrokerProtocolException
from core.dafunk.broker import DaKafkaBroker
from enum import Enum

class Protocol(Enum):
    WEB = 1
    WEBSOCKET = 2
    EVENT = 3

class DaService:
    __slots__ = ("_settings", "_broker", "_events_routes", "_web_routes", "_websockets_routes", "_logger")

    def __init__(self, settings: DaSettings):
        log_filepath = os.path.join(settings.logger.filepath, settings.logger.filename)
        logger.add(log_filepath,
                   format=settings.logger.format,
                   level=settings.logger.level,
                   rotation=settings.logger.rotation,
                   enqueue=True,)
        self._logger: Logger= logger
        self._settings: DaSettings = settings
        self._events_routes: dict[str, Any] = {}
        self._web_routes: dict[str, Any] = {}
        self._websockets_routes: dict[str, Any] = {}

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
                self._logger.trace("Added event route: {}", route)
                self._events_routes[route] = func
            elif protocol == Protocol.WEB:
                self._logger.trace("Added web route: {}", route)
                self._web_routes[route] = func
            elif protocol == Protocol.WEBSOCKET:
                self._logger.trace("Added websocket route: {}", route)
                self._websockets_routes[route] = func
            else:
                self._logger.critical("Unknown protocol: {protocol}", protocol=protocol)
                raise BrokerProtocolException("Protocol not supported")
            return wrapper
        return decorator

    async def receive_events(self,
                             queue: asyncio.Queue):
        self._logger.trace("Starting while loop in events receiver")
        while True:
            event = await queue.get()
            if event is not None:
                topic = event["topic"]
                if topic not in self._events_routes:
                    pass
                else:
                    if topic not in self._events_routes[topic]:
                        self._logger.trace("Event topic: {} exist and would be treated", event["topic"])


                self._logger.debug("Event received: {}", event)
            queue.task_done()

    async def start(self, events_processes: bool = True, web_processes: bool = False, websockets_processes: bool = False):
        self._logger.info("Starting DaFunk service")
        if events_processes:
            self._logger.trace("Preparing Queue for events")
            event_queue = asyncio.Queue()
            self._logger.trace("Calling Consumer")
            consumer = DaKafkaBroker(self._settings.broker, self._logger)
            self._logger.trace("Preparing Gatering Tasks")
            await asyncio.gather(
                event_queue.join(),
                asyncio.create_task(self.receive_events(event_queue)),
                asyncio.create_task(consumer.start(
                    list(self._events_routes.keys()),
                    event_queue))
            )
