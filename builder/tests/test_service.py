import pytest
from faststream.kafka import TestKafkaBroker
from builder.src import broker
from builder.src.message import BuildRequestMessage
from builder.src.service import handler_build



@pytest.mark.asyncio
async def test_handle_kafka_service(monkeypatch):
    async with TestKafkaBroker(broker) as br:

        message = BuildRequestMessage(
            name="builder",
            repository_name="dafunk"
        )
        await br.publish(message, topic="build")
        handler_build.mock.assert_called_with(message.model_dump())

