import os
import uuid
from typing import Annotated

from faststream import FastStream
from faststream.nats import NatsBroker
from pydantic import Field

from builder.models import Config
from builder.db import SessionDep, create_db_and_tables
from builder.utils import get_rand_code, untar_file, get_s3_object

from settings import Settings
broker = NatsBroker("nats://localhost:4222/")
app = FastStream(broker)
actual_path = os.path.dirname(os.path.abspath(__file__))

@broker.subscriber("build")
async def handler_build(
        repository: str = Field(
            ..., examples=['remote_repository/repo.tar.gz'], description="The remote repository filepath"
        ),
        repository_id: uuid.UUID = Field(
            ..., description="The remote repository uuid, the service return that value and maintain traceability of the building process"
        )

) -> str:
    access_key = os.environ.get("AWS_ACCESS_KEY")
    secret_key = os.environ.get("AWS_SECRET_KEY")

    get_s3_object(access_key, secret_key, )
    return f"User: {user_id} - {user} registered"

@app.post("/build")
def config(repository_zip: Annotated[UploadFile, File()], repository_id: int ,
           settings: Annotated[Settings, Depends(get_settings)],
           session: SessionDep) ->list[Config]:

    random_folder = get_rand_code(20)
    file_path = os.path.join(actual_path, random_folder, repository_zip.file.name)
    # upload file
    try:
        content = repository_zip.file.read()
        with open(file_path, "wb") as file:
            file.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # extract the tar file
    try:
        untar_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    results = session.exec(select(Config)).all()

    return results
