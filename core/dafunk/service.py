import asyncio
import functools
import os
import threading
import time
from typing import Any, Union

import orjson
from loguru import logger
from loguru._logger import Logger
from pydantic import BaseModel

from core.dafunk import Settings, BrokerProtocolException, HttpServer, Request
from enum import Enum
from core.dafunk.exceptions import EventMethodError, ServiceException


class Protocol(Enum):
    WEB = 1
    WEBSOCKET = 2
    EVENT = 3


class Service:
    __slots__ = ("_settings", "_broker", "_events_routes", "_web_routes", "_websockets_routes", "_logger")

    def __init__(self, settings: Settings):
        log_filepath = os.path.join(settings.logger.filepath, settings.logger.filename)
        logger.add(log_filepath,
                   format=settings.logger.format,
                   level=settings.logger.level,
                   rotation=settings.logger.rotation,
                   enqueue=True,)
        self._logger: Logger= logger
        self._settings: Settings = settings
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


    def route(self, route: str,
              request: Request = Request.GET,
              protocol: Protocol = Protocol.EVENT,
              model: Union[None, BaseModel] = None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            if protocol == Protocol.EVENT:
                self._logger.trace("Added event route: {}", route)
                if route not in self._events_routes:
                    self._logger.trace("Event Route does not exist: {}", route)
                    self._events_routes[route] = {}
                self._events_routes[route]['func'] = func
                self._events_routes[route]['model'] = model
            elif protocol == Protocol.WEB:
                self._logger.trace("Added web route: {}", route)
                if route not in self._web_routes:
                    self._logger.trace("Web Route does not exist: {}", route)
                    self._web_routes[route] = {}
                self._web_routes[route]['func'] = func
                self._web_routes[route]['request'] = request
                self._web_routes[route]['model'] = model
            elif protocol == Protocol.WEBSOCKET:
                self._logger.trace("Added websocket route: {}", route)
                if route not in self._websockets_routes:
                    self._logger.trace("Websocket Route does not exist: {}", route)
                    self._websockets_routes[route] = {}
                self._websockets_routes[route]['func'] = func
                self._websockets_routes[route]['model'] = model
            else:
                self._logger.critical("Unknown protocol: {protocol}", protocol=protocol)
                raise BrokerProtocolException("Protocol not supported")

            return wrapper
        return decorator

    def start(self, events_processes: bool = True, web_processes: bool = False, websockets_processes: bool = False):
        self._logger.info("Starting DaFunk services..")
        if events_processes:
            from core.dafunk.broker import KafkaBroker
            consumer = KafkaBroker(self._settings.broker, self._logger)
            thread = threading.Thread(target=consumer.start, args=(
                self._events_routes,
            ))
            thread.daemon = True
            thread.start()

        if web_processes:
            async def start_service_web():
                setting_web = self._settings.http
                self._logger.info("Starting HTTP Server {}:{}", setting_web.host
                              , setting_web.port)
                server_http = HttpServer(setting_web)
                server_http.prepare_routes(self._web_routes)
                async with asyncio.TaskGroup() as th:
                    th.create_task(
                        server_http.start()
                    )

            thread_web = threading.Thread(target=asyncio.run, args=(
                start_service_web(),
            ))
            thread_web.daemon = True
            thread_web.start()
        while True:
            time.sleep(10)
            continue
