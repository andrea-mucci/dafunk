import asyncio
from enum import Enum
from typing import Any

from aiohttp import web

from core.dafunk.settings import HttpSettings

class Request(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

class HttpServer:
    __slots__ = ('_settings', "_app")

    def __init__(self, settings: HttpSettings):
        self._settings = settings
        self._app = web.Application()

    def prepare_routes(self, routes: dict[str, Any]) -> None:
        from aiohttp import web
        list_routes = []
        for route, values in routes.items():
            if values['request'] is Request.GET:
                list_routes.append(
                    web.get(route, values['func'])
                )
            elif values['request'] is Request.POST:
                list_routes.append(
                    web.post(route, values['func'])
                )
            elif values['request'] is Request.PUT:
                list_routes.append(
                    web.put(route, values['func'])
                )
            elif values['request'] is Request.DELETE:
                list_routes.append(
                    web.delete(route, values['func'])
                )
        self._app.add_routes(list_routes)

    async def start(self):
        runner = web.AppRunner(self._app)
        await runner.setup()
        site = web.TCPSite(runner, self._settings.host, self._settings.port)
        await site.start()
        while True:
            await asyncio.sleep(3600)
