# #!/usr/bin/env python
#
# """Tests for `dafunk_core_library` package."""
#
# import pytest  # noqa: F401
# import os
#
# from faststream.kafka import KafkaBroker
# from faststream.nats import NatsBroker
#
# from core.dafunk import DaSettings, DaBroker, DaEvent
#
# actual_path = os.path.dirname(os.path.abspath(__file__))
#
#
# def test_message(monkeypatch):
#     event_message = DaEvent()
#     hashmap = event_message.hashmap
#     new_event_message = DaEvent(hashmap=hashmap)
#     assert new_event_message.hashmap == hashmap
