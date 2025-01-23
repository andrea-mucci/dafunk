import os
import uuid
from typing import Annotated

from faststream import FastStream
from pydantic import Field

from builder.utils import get_s3_object
from core.dafunk import DaSettings, DaBroker

actual_path = os.path.dirname(os.path.abspath(__file__))
settings_file = os.path.join(actual_path, "settings.json")
settings_object = DaSettings.load_from_file(settings_file)
settings = settings_object.settings
broker = DaBroker.from_settings(settings)

app = FastStream(broker)


@broker.subscriber("build")
async def handler_build(
        repository: str = Field(
            ..., examples=['remote_repository/repo.tar.gz'], description="The remote repository filepath"
        ),
        repository_id: uuid.UUID = Field(
            ..., description="The remote repository uuid, the service return that value and maintain traceability of the building process"
        )

) -> str:

    get_s3_object(access_key, secret_key, )
    return f"User: {user_id} - {user} registered"
