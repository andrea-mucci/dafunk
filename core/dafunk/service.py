import functools
import os
import threading
import time
from typing import Any, Union
from loguru import logger
from loguru._logger import Logger
from pydantic import BaseModel
from starlette._utils import is_async_callable

from core.dafunk import Settings, BrokerProtocolException, HttpServer, HttpRequest, Database, Message
from enum import Enum

from core.dafunk.broker import KafkaBroker


class Protocol(Enum):
    WEB = 1
    WEBSOCKET = 2
    EVENT = 3


class Service:
    __slots__ = ("_settings", "_broker", "_events_routes", "_web_routes", "_websockets_routes", "_logger", "_db")

    def __init__(self, settings: Settings):
        log_filepath = os.path.join(settings.logger.filepath, settings.logger.filename)
        logger.add(log_filepath,
                   format=settings.logger.format,
                   level=settings.logger.level,
                   rotation=settings.logger.rotation,
                   enqueue=True,)
        self._logger: Logger= logger
        self._settings: Settings = settings
        self._db: Database = None
        self._events_routes: dict[str, Any] = {}
        self._web_routes: dict[str, Any] = {}
        self._websockets_routes: dict[str, Any] = {}

    def send_event(self, topic: str, content: Union[str, int, float, dict, list, BaseModel]) -> None:
        message_to_send = Message(
            payload=content
        )
        KafkaBroker.producer(
            topic=topic,
            message=message_to_send,
            settings=self._settings.broker
        )

    @property
    def db(self) -> Database:
        return self._db

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

    def _prepare_db(self) -> Database | None:
        database = self._settings.database
        db = None
        if database.status:
            self._logger.info("Database connection enabled")
            db = Database(database)
            db.create_tables()
        return db

    def route(self, route: str,
              request: HttpRequest = HttpRequest.GET,
              protocol: Protocol = Protocol.EVENT,
              model: Union[None, BaseModel] = None):
        def decorator(func):
            self._logger.debug("Added route protocol {}", protocol.value)
            if protocol.value == 3:
                self._logger.trace("Added event route: {}", route)
                if route not in self._events_routes:
                    self._logger.trace("Event Route does not exist: {}", route)
                    self._events_routes[route] = {}
                self._events_routes[route]['func'] = func
                self._events_routes[route]['model'] = model
            elif protocol.value == 1:
                self._logger.trace("Added web route: {}", route)
                if route not in self._web_routes:
                    self._logger.trace("Web Route does not exist: {}", route)
                    self._web_routes[route] = []
                data = {}
                data['func'] = func
                data['request'] = request
                data['model'] = model
                self._web_routes[route].append(data)
            elif protocol.value == 2:
                self._logger.trace("Added websocket route: {}", route)
                if route not in self._websockets_routes:
                    self._logger.trace("Websocket Route does not exist: {}", route)
                    self._websockets_routes[route] = {}
                self._websockets_routes[route]['func'] = func
                self._websockets_routes[route]['model'] = model
            else:
                self._logger.critical("Unknown protocol: {protocol}", protocol=protocol)
                raise BrokerProtocolException("Protocol not supported")
            if is_async_callable(func):
                @functools.wraps(func)
                async def async_wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)
                return async_wrapper
            else:
                @functools.wraps(func)
                def sync_wrapper(*args, **kwargs):
                    return func(*args, **kwargs)
                return sync_wrapper
        return decorator

    def start(self, events_processes: bool = True, web_processes: bool = False, websockets_processes: bool = False):
        self._logger.info("Starting DaFunk services..")
        self._db = self._prepare_db()
        if events_processes:
            from core.dafunk.broker import KafkaBroker
            consumer = KafkaBroker(self._settings.broker, self._logger)
            thread = threading.Thread(target=consumer.start, args=(
                self._events_routes,
            ))
            thread.daemon = True
            thread.start()

        if web_processes:
            setting_web = self._settings.http

            self._logger.info("Starting HTTP Server {}:{}", setting_web.host
                              , setting_web.port)
            server_http = HttpServer(setting_web)
            server_http.prepare_routes(self._web_routes)
            thread_web = threading.Thread(target=server_http.start)
            thread_web.daemon = True
            thread_web.start()
        while True:
            time.sleep(10)
            continue
