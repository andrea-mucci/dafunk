import os
from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends, File
from sqlmodel import select
from starlette.datastructures import UploadFile

from builder.models import Config
from builder.db import SessionDep, create_db_and_tables
from builder.utils import get_rand_code, untar_file

from settings import Settings

app = FastAPI()
actual_path = os.path.dirname(os.path.abspath(__file__))

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@lru_cache
def get_settings():
    return Settings()
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
