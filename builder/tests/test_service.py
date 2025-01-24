import pytest
from faststream.nats import TestNatsBroker
from pydantic import ValidationError

from builder.src.service import handler_build
from builder.src import broker, BuildMessage


@pytest.mark.asyncio
async def test_handle_nats_service():
    async with TestNatsBroker(broker) as br:
        message = BuildMessage(
            repository_name="dafunk"
        )
        await br.publish(message, subject="build")
        handler_build.mock.assert_called_with(message.model_dump())

@pytest.mark.asyncio
async def test_handle_nats_service_message_exception():
    async with TestNatsBroker(broker) as br:
        with pytest.raises(ValidationError):
            message = BuildMessage(
                repository_name="dafunk",
                wrong_field="hello"
            )
            await br.publish(message, subject="build")
            handler_build.mock.assert_called_with(message.model_dump())
