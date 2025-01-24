import os
import uuid
from faststream import FastStream
from pydantic import Field

from builder.src import BuildMessage
from core.dafunk import DaSettings, DaBroker

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
settings_file = os.path.join(parent_path, "settings.yaml")
settings_object = DaSettings.load_from_file(settings_file)
settings = settings_object.settings
broker = DaBroker.from_settings(settings)

app = FastStream(broker)


@broker.subscriber("build")
async def handler_build(
        repository: BuildMessage,
) -> str:
    return f"sucalo"
