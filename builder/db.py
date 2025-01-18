from typing import Annotated

from fastapi import Depends

from builder.settings import Settings
from sqlmodel import create_engine, Session, SQLModel

settings = Settings()
connect_args = {"check_same_thread": False}
engine = create_engine(settings.db_url, connect_args=connect_args)


def get_session() -> Session:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]