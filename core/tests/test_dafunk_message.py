#!/usr/bin/env python
import pytest

from core.dafunk import DaMessage

def test_message_class_payload_float():
    message = DaMessage(
        uuid="12345",
        payload=23.6
    )
    bytes = message.get_bites()
    assert bytes == b'{"uuid":"12345","payload":23.6}'

def test_message_class_payload_integer():
    message = DaMessage(
        uuid="12345",
        payload=23
    )
    bytes = message.get_bites()
    assert bytes == b'{"uuid":"12345","payload":23}'

def test_message_class_payload_text():
    message = DaMessage(
        uuid="12345",
        payload="hello dafunk"
    )
    bytes = message.get_bites()
    assert bytes == b'{"uuid":"12345","payload":"hello dafunk"}'

def test_message_class_payload_dict():
    message = DaMessage(
        uuid="12345",
        payload={"test": "this is a test"}
    )
    bytes = message.get_bites()
    assert bytes == b'{"uuid":"12345","payload":{"test":"this is a test"}}'

