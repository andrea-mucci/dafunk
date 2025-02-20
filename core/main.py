import asyncio
import os

from aiohttp import web
from pydantic import BaseModel

from core.dafunk import Settings, Service, Protocol, Request

actual_path = os.path.dirname(os.path.abspath(__file__))


class EventReceived(BaseModel):
    id: int
    name: str

def main():
    json_dict = {
        "default": {
            'broker': {
                'auto_offset': True,
                'group': 'ServiceGroup',
                'log_level': 6,
                'max_bytes': 1000000,
                'num_partitions': 1,
                'offset_reset': 'latest',
                'receive_max_bytes': 100000000,
                'replication_factor': 1,
                'session_timeout': 6000,
                'url': "localhost:9092"
            },
            'database': {
                'host': None,
                'password': None,
                'port': None,
                'url': 'postgresql+psycopg://scott:tiger@localhost/tester',
                'username': None
            },
            'logger': {
                'filename': 'dafunk_service.log',
                'filepath': './logs',
                'format': '<green>{time:D/M/YY HH:mm}</green>Z - '
                          '<blue>{level}</blue> - {message}',
                'level': 'DEBUG',
                'rotation': '10 MB'
            },
            'storage': {
                'access_key': 'AKIA3NVLPTX6UUORHIUO',
                'bucket': 'dafunk',
                'region': 'eu-west-1',
                'secret_key': 'xgYdjmpjSNyYRFIjyKxqKBwBtj/YwwFvzTsKVAL+',
                'storage': None
            },
            'http': {'status': True, 'host': 'localhost', 'port': 8000},
        }
    }
    object_settings = Settings.load_from_json(json_dict)
    service = Service(object_settings)

    @service.route("/test",
                   request=Request.GET,
                   protocol=Protocol.WEB)
    def test(request):
        return web.Response(text="Hello, world")

    @service.route("/other/test",
                   request=Request.POST,
                   protocol=Protocol.WEB)
    def other_test(request):
        return "ciao"

    @service.route("event_test", model=EventReceived)
    def event_test(message_dict: EventReceived):
        return "ciao"

    @service.route("other_event_test", model=EventReceived)
    def other_event_test(message_dict: EventReceived):
        return "miao"

    service.start(
        events_processes=True, web_processes=True
    )

if __name__ == '__main__':
    main()
