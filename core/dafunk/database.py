from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from core.dafunk.settings import DatabaseSettings

class Base(DeclarativeBase):
    pass

class Database:
    __slots__ = ['_settings', '_connection_args', '_engine']

    def __init__(self, config: DatabaseSettings):
        self._settings = config
        self._connection_args = {}
        self._engine = None

    @property
    def Session(self):
        if self._engine is None:
            self._create_engine()
        return sessionmaker(bind=self._engine)

    def _prepare_dns(self):
        if self._settings.url is not None:
            return self._settings.url
        else:
            # check if the name is
            dns = ""
            name = self._settings.name
            username = self._settings.username
            password = self._settings.password
            host = self._settings.host
            port = self._settings.port
            dns = f"postgresql+psycopg://{username}:{password}@{host}:{port}/{name}"
            return dns

    def _create_engine(self):
        dns = self._prepare_dns()
        if len(self._connection_args) > 0:
            self._engine = create_engine(dns, connect_args=self._connection_args)
        else:
            self._engine = create_engine(dns)

    def create_tables(self):
        if self._engine is None:
            self._create_engine()
        Base.metadata.create_all(self._engine)
