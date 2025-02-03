from typing import TypeVar, Type, Self, Optional, Any

import yaml
from pydantic import BaseModel, Field
import os

from core.dafunk.utils import dict_keys_lower

class LoggerSettings(BaseModel):
    format: Optional[str] = Field("<green>{time:D/M/YY HH:mm}</green>Z - <blue>{level}</blue> - {message}",
                                  description="Logger format")
    level: Optional[str] = Field("DEBUG", description="Logger level")
    filepath: Optional[str] = Field("./logs", description="Logger file path")
    filename: Optional[str] = Field("dafunk_service.log", description="Logger file name")
    rotation: Optional[str] = Field("10 MB", description="Logger rotation sizeyoutu"
                                                         "")

class BrokerSettings(BaseModel):
    url: str = Field(..., description="Broker ulr or list of brokers urls")
    group: str = Field("ServiceGroup", description="Broker group")
    session_timeout: Optional[int] = Field(6000, description="Session timeout")
    offset_reset: Optional[str] = Field('latest', description="Broker offset reset")
    auto_offset: Optional[bool] = Field(True, description="Auto offset")
    max_bytes: Optional[int] = Field(1000000, description="Message max bytes")
    receive_max_bytes: Optional[int] = Field(100000000, description="Message receive maxbytes")
    log_level: Optional[int] = Field(6, description="Log level from 0 to 7")
    num_partitions: Optional[int] = Field(1, description="Number of partitions")
    replication_factor: Optional[int] = Field(1, description="Replication factor")

class StorageSettings(BaseModel):
    storage: Optional[str] = Field(None, description="One of the suppoorted storages: local or s3 compatible")
    bucket: Optional[str] = Field(None, description="Bucket name")
    region: Optional[str] = Field(None, description="AWS region")
    access_key: Optional[str] = Field(None, description="AWS/S3 compatible access key")
    secret_key: Optional[str] = Field(None, description="AWS/S3 compatible secret key")

class DatabaseSettings(BaseModel):
    url: Optional[str] = Field(None, description="Database url")
    username: Optional[str] = Field(None, description="Database username")
    password: Optional[str] = Field(None, description="Database password")
    port: Optional[int] = Field(None, description="Database port")
    host: Optional[str] = Field(None, description="Database host")

class BaseSettings(BaseModel):
    database: Optional[DatabaseSettings] = Field(None, description="The Database configuration settings")
    storage: Optional[StorageSettings] = Field(
        default=None,
        description="The Storage configuration settings"
    )
    broker: Optional[BrokerSettings] = Field(
        default=None,
        description="Broker Configurations"
    )
    logger: Optional[LoggerSettings] = Field(
        LoggerSettings(),
        description="Logger status active or inactive"
    )

class StagingSettings(BaseModel):
    default: Optional[BaseSettings]
    test: Optional[BaseSettings]
    dev: Optional[BaseSettings]
    stag: Optional[BaseSettings]
    prod: Optional[BaseSettings]


TBaseSetting = TypeVar("TBaseSetting", bound=BaseSettings)
TStagingSetting = TypeVar("TStagingSetting", bound=StagingSettings)


class DaSettings(object):
    _prefix: str = "DAFUNK_"

    def __init__(self, file_name: str = None):
        if file_name is not None:
            stream = open(file_name, "r", encoding="utf-8")
            self._settings = yaml.load(stream, Loader=yaml.FullLoader)
            self._object_model = None
        # merge settings with env variables
        dict_env_variables = self._load_environment_variables()
        dict_env_variables = dict_keys_lower(dict_env_variables)
        stage = None
        if "staging" in dict_env_variables:
            stage = dict_env_variables["staging"]
            del dict_env_variables["staging"]
        self._settings = self._parse_stages(stage)
        dict_env_variables = self._format_environment_variables(dict_env_variables)
        if isinstance(self._settings, dict) and isinstance(dict_env_variables, dict):
            self._settings.update(dict_env_variables)

    @property
    def broker(self) -> BrokerSettings:
        return self._object_model.broker

    @property
    def database(self) -> DatabaseSettings:
        return self._object_model.database

    @property
    def logger(self) -> DatabaseSettings:
        return self._object_model.logger

    def _parse_stages(self, stage=None) -> dict:
        if "default" in self._settings:
            settings = self._settings["default"]
        else:
            settings = {}
        if stage is not None and stage in self._settings:
            settings.update(self._settings[stage])
        return settings

    def _load_environment_variables(self, prefix: str = None) -> dict:
        new_dict = {}
        if prefix is not None:
            self._prefix = prefix

        for name, value in os.environ.items():
            if name.startswith(self._prefix):
                name = name.replace(self._prefix, "", 1)
                new_dict[name] = value
        return new_dict

    def _format_environment_variables(self, env_variables: dict[str, Any]) -> dict:
        new_dict_envs = {}
        for name, value in env_variables.items():
            root_name = name.split("_", 1)
            if root_name[0] in self._settings:
                if not root_name[0] in new_dict_envs:
                    new_dict_envs[root_name[0]] = {}
                new_dict_envs[root_name[0]][root_name[1]] = value
            else:
                new_dict_envs[name] = value
        return new_dict_envs



    def _load_to_model(self, model: Type[TBaseSetting]):
        self._object_model = model(**self._settings)

    @property
    def to_json(self) -> dict:
        return self._object_model.model_dump()

    @classmethod
    def load_from_file(
        cls, file_name: str, settings_model: Type[TBaseSetting] = BaseSettings
    ) -> Self:
        object_settings = cls(file_name)
        object_settings._load_to_model(settings_model)
        return object_settings
