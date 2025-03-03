from enum import Enum
from typing import Any

import uvicorn
from fastapi import FastAPI, APIRouter

from core.dafunk import HttpServerException
from core.dafunk.database import Database
from core.dafunk.settings import HttpSettings

class Request(Enum):
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

class HttpServer:
    __slots__ = ('_settings', "_app", "_router", "_db")

    def __init__(self, settings: HttpSettings, db_object: Database = None):
        self._settings = settings
        self._app = FastAPI()
        self._router = APIRouter()
        self._db = db_object


    def prepare_routes(self, routes: dict[list[str, Any]]) -> None:

        for route, values in routes.items():
            for value in values:
                if value['request'] is Request.GET:
                    self._router.add_api_route(
                        path=route,
                        endpoint=value['func'],
                        methods=['GET']
                    )

                elif value['request'] is Request.POST:
                    self._router.add_api_route(
                        path=route,
                        endpoint=value['func'],
                        methods=['POST']
                    )
                elif value['request'] is Request.PUT:
                    self._router.add_api_route(
                        path=route,
                        endpoint=value['func'],
                        methods=['PUT']
                    )
                elif value['request'] is Request.DELETE:
                    self._router.add_api_route(
                        path=route,
                        endpoint=value['func'],
                        methods=['DELETE']
                    )
                else:
                    raise HttpServerException("Request Method {} invalid".format(values['request']))

    def start(self):
       self._app.include_router(self._router)
       uvicorn.run(self._app, host=self._settings.host, port=self._settings.port)

