#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""

import pytest  # noqa: F401
import os

from faststream.kafka import KafkaBroker
from faststream.nats import NatsBroker

from core.dafunk import DaSettings, DaBroker

actual_path = os.path.dirname(os.path.abspath(__file__))


def test_broker_nat(monkeypatch):
    settings_file = os.path.join(actual_path, "fixtures", "settings_broker.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    broker = DaBroker.from_settings(object_settings.settings)
    assert isinstance(broker, NatsBroker) == True

def test_broker_kafka(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "test")
    settings_file = os.path.join(actual_path, "fixtures", "settings_broker.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    broker = DaBroker.from_settings(object_settings.settings)
    assert isinstance(broker, KafkaBroker) == True


