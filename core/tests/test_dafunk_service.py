#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""
from asyncio import run

import pytest  # noqa: F401
import os

from core.dafunk import DaSettings
from core.dafunk.service import DaService
from core.dafunk.utils import TestKafkaContainer

actual_path = os.path.dirname(os.path.abspath(__file__))

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

def test_service_start():
    settings_file = os.path.join(actual_path, "fixtures", "settings_broker.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    service = DaService(object_settings)

    @service.route("test")
    def test():
        return "ciao"

    @service.route("other_test")
    def other_test():
        return "miao"
    run(service.start())
    assert "ciao" == "miao"

@pytest.mark.asyncio
async def test_service_event():
    with TestKafkaContainer(port=9092) as kafka_container:
        broker_url, broker_port = kafka_container.get_bootstrap_servers()

        assert False == True


