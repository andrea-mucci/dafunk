#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""

import pytest  # noqa: F401
import os
from core.dafunk import DaSettings

actual_path = os.path.dirname(os.path.abspath(__file__))


def test_settings_class_merge_env(monkeypatch):
    monkeypatch.setenv(
        "DAFUNK_DB_URL", "postgresql+psycopg://scott:tiger@localhost/tester"
    )
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        "db_url": "postgresql+psycopg://scott:tiger@localhost/tester",
        "broker_url": "nats://localhost:4222",
        "logger": False,
        "logger_url": "https://localhost:4034",
    }


def test_settings_class_merge_multiple_env(monkeypatch):
    monkeypatch.setenv(
        "DAFUNK_DB_URL", "postgresql+psycopg://scott:tiger@localhost/tester"
    )
    monkeypatch.setenv("DAFUNK_LOGGER", "true")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        "db_url": "postgresql+psycopg://scott:tiger@localhost/tester",
        "broker_url": "nats://localhost:4222",
        "logger": True,
        "logger_url": "https://localhost:4034",
    }


def test_settings_class_test_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "test")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        "db_url": "sqlite:///test_db.db",
        "broker_url": "nats://localhost:4222",
        "logger": False,
        "logger_url": "https://localhost:4034",
    }


def test_settings_class_dev_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "dev")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        "db_url": "postgresql+psycopg://scott:tiger@dev.example.com/test",
        "broker_url": "nats://dev.example.com:4222",
        "logger": False,
        "logger_url": "https://localhost:4034",
    }


def test_settings_class_stag_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "stag")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        "db_url": "postgresql+psycopg://john:doe@stag.example.com/test",
        "broker_url": "nats://stag.example.com:4222",
        "logger": False,
        "logger_url": "https://localhost:4034",
    }


def test_settings_class_prod_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "prod")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        "db_url": "postgresql+psycopg://scott:tiger@prod.example.com/test",
        "broker_url": "nats://prod.example.com:4222",
        "logger": False,
        "logger_url": "https://localhost:4034",
    }
