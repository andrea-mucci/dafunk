import os
import uuid

from faststream import FastStream

from builder.src.message import BuildRequestMessage, BuildResponseMessage
from core.dafunk import DaSettings, DaBroker

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
settings_file = os.path.join(parent_path, "settings.yaml")
settings_object = DaSettings.load_from_file(settings_file)
settings = settings_object.settings
broker = DaBroker.from_settings(settings)
app = FastStream(broker)


@broker.subscriber("build")
@broker.publisher("build:complete")
async def handler_build(
        repository: BuildRequestMessage,
) -> BuildResponseMessage:
    response = BuildResponseMessage(
        build_id=str(uuid.uuid4()),
        status="completed"
    )
    return response
