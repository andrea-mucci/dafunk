#!/usr/bin/env python

"""Tests for `dafunk_core_library` package."""

import pytest  # noqa: F401
import os
from core.dafunk import DaSettings

actual_path = os.path.dirname(os.path.abspath(__file__))


def test_settings_class_merge_env(monkeypatch):
    monkeypatch.setenv(
        "DAFUNK_DATABASE_URL", "postgresql+psycopg://scott:tiger@localhost/tester"
    )
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.to_json == {'broker': {'auto_offset': False,
            'group': None,
            'log_level': 6,
            'max_bytes': 1000000,
            'offset_reset': 'earliest',
            'receive_max_bytes': 100000000,
            'session_timeout': 6000,
          'replication_factor': 1,
          'num_partitions': 1,
            'url': 'nats://localhost:4222'},
             'database': {'host': None,
                          'password': None,
                          'port': None,
                          'url': 'postgresql+psycopg://scott:tiger@localhost/tester',
                          'username': None},
             'logger': {'level': 'INFO', 'status': False},
             'storage': {'access_key': 'AKIA3NVLPTX6UUORHIUO',
                         'bucket': 'dafunk',
                         'region': 'eu-west-1',
                         'secret_key': 'xgYdjmpjSNyYRFIjyKxqKBwBtj/YwwFvzTsKVAL+',
                         'storage': None}}


def test_settings_class_merge_multiple_env(monkeypatch):
    monkeypatch.setenv(
        "DAFUNK_DATABASE_URL", "postgresql+psycopg://scott:tiger@localhost/tester"
    )
    monkeypatch.setenv("DAFUNK_LOGGER_STATUS", "true")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.to_json == {'broker': {'auto_offset': False,
            'group': None,
            'log_level': 6,
            'max_bytes': 1000000,
            'offset_reset': 'earliest',
            'receive_max_bytes': 100000000,
            'session_timeout': 6000,
                                                  'replication_factor': 1,
          'num_partitions': 1,
            'url': 'nats://localhost:4222'},
             'database': {'host': None,
                          'password': None,
                          'port': None,
                          'url': 'postgresql+psycopg://scott:tiger@localhost/tester',
                          'username': None},
             'logger': {'level': 'INFO', 'status': True},
             'storage': {'access_key': 'AKIA3NVLPTX6UUORHIUO',
                         'bucket': 'dafunk',
                         'region': 'eu-west-1',
                         'secret_key': 'xgYdjmpjSNyYRFIjyKxqKBwBtj/YwwFvzTsKVAL+',
                         'storage': None}}


def test_settings_class_test_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "test")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.to_json == {'broker': {'auto_offset': False,
            'group': None,
            'log_level': 6,
            'max_bytes': 1000000,
            'offset_reset': 'earliest',
            'receive_max_bytes': 100000000,
                                                  'replication_factor': 1,
                                                  'num_partitions': 1,
            'session_timeout': 6000,
            'url': 'nats://localhost:4222'},
             'database': {'host': None,
                          'password': None,
                          'port': None,
                          'url': 'sqlite:///test_db.db',
                          'username': None},
             'logger': {'level': 'INFO', 'status': False},
             'storage': {'access_key': 'AKIA3NVLPTX6UUORHIUO',
                         'bucket': 'dafunk',
                         'region': 'eu-west-1',
                         'secret_key': 'xgYdjmpjSNyYRFIjyKxqKBwBtj/YwwFvzTsKVAL+',
                         'storage': None}}


def test_settings_class_dev_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "dev")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.to_json == {'broker': {'auto_offset': False,
            'group': None,
            'log_level': 6,
            'max_bytes': 1000000,
            'offset_reset': 'earliest',
            'receive_max_bytes': 100000000,
                                                  'replication_factor': 1,
                                                  'num_partitions': 1,
            'session_timeout': 6000,
            'url': 'nats://dev.example.com:4222'},
             'database': {'host': None,
                          'password': None,
                          'port': None,
                          'url': 'postgresql+psycopg://scott:tiger@dev.example.com/test',
                          'username': None},
             'logger': {'level': 'INFO', 'status': False},
             'storage': {'access_key': 'AKIA3NVLPTX6UUORHIUO',
                         'bucket': 'dafunk',
                         'region': 'eu-west-1',
                         'secret_key': 'xgYdjmpjSNyYRFIjyKxqKBwBtj/YwwFvzTsKVAL+',
                         'storage': None}}


def test_settings_class_stag_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "stag")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.to_json == {'broker': {'auto_offset': False,
            'group': None,
            'log_level': 6,
            'max_bytes': 1000000,
            'offset_reset': 'earliest',
            'receive_max_bytes': 100000000,
                                                  'replication_factor': 1,
                                                  'num_partitions': 1,
            'session_timeout': 6000,
            'url': 'nats://stag.example.com:4222'},
             'database': {'host': None,
                          'password': None,
                          'port': None,
                          'url': 'postgresql+psycopg://john:doe@stag.example.com/test',
                          'username': None},
             'logger': {'level': 'INFO', 'status': False},
             'storage': {'access_key': 'AKIA3NVLPTX6UUORHIUO',
                         'bucket': 'dafunk',
                         'region': 'eu-west-1',
                         'secret_key': 'xgYdjmpjSNyYRFIjyKxqKBwBtj/YwwFvzTsKVAL+',
                         'storage': None}}


def test_settings_class_prod_staging(monkeypatch):
    monkeypatch.setenv("DAFUNK_STAGING", "prod")
    settings_file = os.path.join(actual_path, "fixtures", "settings.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    assert object_settings.to_json == {'broker': {'auto_offset': False,
            'group': None,
            'log_level': 6,
            'max_bytes': 1000000,
            'offset_reset': 'earliest',
            'receive_max_bytes': 100000000,
                                                  'replication_factor': 1,
                                                  'num_partitions': 1,
            'session_timeout': 6000,
            'url': 'nats://prod.example.com:4222'},
             'database': {'host': None,
                          'password': None,
                          'port': None,
                          'url': 'postgresql+psycopg://scott:tiger@prod.example.com/test',
                          'username': None},
             'logger': {'level': 'INFO', 'status': False},
             'storage': {'access_key': 'AKIA3NVLPTX6UUORHIUO',
                         'bucket': 'dafunk',
                         'region': 'eu-west-1',
                         'secret_key': 'xgYdjmpjSNyYRFIjyKxqKBwBtj/YwwFvzTsKVAL+',
                         'storage': None}}
