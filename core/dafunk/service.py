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

    async def receive_events(self,
                             queue: asyncio.Queue):
        self._logger.trace("Starting while loop in events receiver")
        while True:
            event = await queue.get()
            if event is not None:
                topic = event["topic"]
                content = event["content"]
                self._logger.debug("Received event in queue with topic: {}", topic)
                if topic not in self._events_routes:
                    self._logger.trace("The topic does not exit: {}", topic)
                    pass
                else:
                    self._logger.debug("The topic exit: {} and value {}", topic, content)
                    try:
                        funct = self._events_routes[topic]['func']
                        message_dict = orjson.loads(content)
                        if self._events_routes[topic]['model'] is not None:
                            model = self._events_routes[topic]['model']
                            message_data = model(**message_dict['payload'])
                        else:
                            message_data = message_dict['payload']
                        funct(message_data)
                    except EventMethodError as e:
                        self._logger.error("EventMethodError: {}".format(e))
                        raise ServiceException("The route returned an error: {}".format(e))
                    except Exception as e:
                        self._logger.error("Generic Error: {}".format(e))
                        raise ServiceException("The route returned a generic error: {}".format(e))

            queue.task_done()

    def start(self, events_processes: bool = True, web_processes: bool = False, websockets_processes: bool = False):
        self._logger.info("Starting DaFunk services..")
        if events_processes:
            async def start_service_broker():
                from core.dafunk.broker import KafkaBroker
                self._logger.info("Starting Event Consumer....")
                self._logger.trace("Preparing Queue for events")
                event_queue = asyncio.Queue()
                self._logger.trace("Calling Consumer")
                consumer = KafkaBroker(self._settings.broker, self._logger)
                self._logger.trace("Preparing Gatering Tasks")
                async with asyncio.TaskGroup() as th:
                    th.create_task(
                        event_queue.join()
                    )
                    th.create_task(
                        self.receive_events(event_queue)
                    )
                    th.create_task(
                        consumer.start(
                            list(self._events_routes.keys()),
                        event_queue)
                    )

            thread = threading.Thread(target=asyncio.run, args=(
                start_service_broker(),
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
