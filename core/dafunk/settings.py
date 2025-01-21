from typing import TypeVar, Type, Self

import yaml
from pydantic import BaseModel, Field
import os

from core.dafunk.utils import dict_keys_lower


class BaseSettings(BaseModel):
    db_url: str = Field(..., description="The database url",
                        examples=["postgresql+psycopg://scott:tiger@localhost/test",])
    broker_url: str = Field(..., description="Event Broker url, we support NATS, RabbitMQ, Kafka, Redis")
    logger: bool = Field(False, description="Logger status active or inactive")
    logger_url: str = Field(..., description="Internal logger url")

TBaseSetting = TypeVar("TBaseSetting", bound=BaseSettings)

class DaSettings(object):
    _prefix: str = "DAFUNK_"

    def __init__(self, file_name: str = None):
        if file_name is not None:
            stream = open(file_name, 'r', encoding='utf-8')
            self._settings = yaml.load(stream, Loader=yaml.FullLoader)
            self._object_model = None
        # merge settings with env variables
        dict_env_variables = self._load_environment_variables()
        dict_env_variables = dict_keys_lower(dict_env_variables)
        if isinstance(self._settings, dict) and isinstance(dict_env_variables, dict):
            self._settings.update(
                dict_env_variables
            )

    def _load_environment_variables(self, prefix: str = None) -> dict:
        new_dict = {}
        if prefix is not None:
            self._prefix = prefix

        for name, value in os.environ.items():
            if name.startswith(self._prefix):
                name = name.replace(self._prefix, '', 1)
                new_dict[name] = value
        return new_dict

    def _load_to_model(self, model: Type[TBaseSetting]):
        self._object_model = model(**self._settings)

    @property
    def settings(self) -> dict:
        return self._object_model.model_dump()


    @classmethod
    def load_from_file(cls, file_name: str, settings_model: Type[TBaseSetting] = BaseSettings) -> Self:
        object_settings = cls(file_name)
        object_settings._load_to_model(settings_model)
        return object_settings

