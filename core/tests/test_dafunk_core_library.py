#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""
import pytest
import os
from core.dafunk import DaSettings

actual_path = os.path.dirname(os.path.abspath(__file__))


def test_settings_class():
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        'db_url': 'postgresql+psycopg://scott:tiger@localhost/test',
        'broker_url': 'nats://localhost:4222',
        'logger': False,
        'logger_url': 'https://localhost:4034'}


def test_settings_class_merge_env(monkeypatch):
    monkeypatch.setenv("DAFUNK_DB_URL",
                       "postgresql+psycopg://scott:tiger@localhost/tester")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        'db_url': 'postgresql+psycopg://scott:tiger@localhost/tester',
        'broker_url': 'nats://localhost:4222',
        'logger': False,
        'logger_url': 'https://localhost:4034'}


def test_settings_class_merge_multiple_env(monkeypatch):
    monkeypatch.setenv("DAFUNK_DB_URL",
                       "postgresql+psycopg://scott:tiger@localhost/tester")
    monkeypatch.setenv("DAFUNK_LOGGER", "true")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.settings == {
        'db_url': 'postgresql+psycopg://scott:tiger@localhost/tester',
        'broker_url': 'nats://localhost:4222',
        'logger': True,
        'logger_url': 'https://localhost:4034'}
