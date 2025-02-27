from boto3 import Session


from core.dafunk.settings import DatabaseSettings
from sqlmodel import create_engine, SQLModel, Session

class Database:
    __slots__ = ['_settings', '_connection_args', '_engine']
    def __init__(self, config: DatabaseSettings):
        self._settings = config
        self._connection_args = {}
        self._engine = None


    def _prepare_dns(self):
        if self._settings.url is not None:
            return self._settings.url
        else:
            # check if the name is
            dns = ""
            name = self._settings.name
            name_db, extension = name.split('.')
            if extension == 'db':
                # the database is an sqlite
                dns = f'sqlite:///{name}'
                self._connection_args['check_same_thread'] = False
            else:
                # this is postgresql
                username = self._settings.username
                password = self._settings.password
                name = self._settings.name
                host = self._settings.host
                port = self._settings.port
                dns = f"postgresql://{username}:{password}@{host}:{port}/{name}"
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
        SQLModel.metadata.create_all(self._engine)

    def get_session(self):
        if self._engine is None:
            self._create_engine()
        with Session(self._engine) as session:
            yield session

