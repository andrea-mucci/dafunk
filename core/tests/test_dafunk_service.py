#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""
import asyncio
import threading
import time

import pytest  # noqa: F401
import os

from loguru import logger
from pydantic import BaseModel
from testcontainers.kafka import KafkaContainer

from core.dafunk import DaSettings
from core.dafunk.broker import DaKafkaBroker
from core.dafunk.service import DaService

actual_path = os.path.dirname(os.path.abspath(__file__))
IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"

@pytest.fixture(scope="module", autouse=True)
def kafka(request):
    kafka = KafkaContainer()
    kafka.start()

    def teardown():
        kafka.stop()

    request.addfinalizer(teardown)
    os.environ["BOOTSTRAP"] = kafka.get_bootstrap_server()

@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="The test that need a Docker Container, must be launched on local")
def test_service_routes():
    settings_file = os.path.join(actual_path, "fixtures", "settings_broker.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    service = DaService(object_settings)

    @service.route("test")
    def test():
        return "ciao"

    @service.route("other_test")
    def other_test():
        return "miao"
    events = service.events_routes
    assert ['test', 'other_test'] == events

@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="The test that need a Docker Container, must be launched on local")
def test_service_event():

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
                'url': os.environ["BOOTSTRAP"]
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
            }
        }
    }
    settings = DaSettings.load_from_json(json_dict)
    service = DaService(settings)

    @service.route("test")
    def test(message_dict: dict):
        assert message_dict == {"key": "da", "value": "funk"}

    @service.route("other_test")
    def other_test():
        return "miao"
    thread = threading.Thread(target=asyncio.run, args=(service.start(),))
    thread.daemon = True
    thread.start()
    time.sleep(10)
    DaKafkaBroker.producer('test', {"key": "da", "value": "funk"}, settings.broker, logger)
    time.sleep(15)


@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="The test that need a Docker Container, must be launched on local")
def test_service_event():

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
                'url': os.environ["BOOTSTRAP"]
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
            }
        }
    }
    settings = DaSettings.load_from_json(json_dict)
    service = DaService(settings)
    class EventReceived(BaseModel):
        id: int
        name: str

    @service.route("test", model=EventReceived)
    def test(message_dict: EventReceived):
        assert message_dict.model_dump() == {"key": "da", "value": "funk"}


    thread = threading.Thread(target=asyncio.run, args=(service.start(),))
    thread.daemon = True
    thread.start()
    time.sleep(10)
    DaKafkaBroker.producer('test', EventReceived(id=1, name="dafunk"), settings.broker, logger)
    time.sleep(15)
