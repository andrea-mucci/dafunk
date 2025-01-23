import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from core.dafunk import StorageUploadException, StorageDeleteException
from core.dafunk.storages.base import BaseStorage


class S3Storage(BaseStorage):

    def __init__(self, access_key: str, secret_key: str, bucket: str, region: str):
        self._client = None
        self._region = region
        self._bucket = bucket
        self._access_key = access_key
        self._secret_key = secret_key


    @classmethod
    def from_settings(cls, settings: dict):
        bucket: str = settings.get('storage_bucket')
        region: str = settings.get('storage_region')
        access_key: str = settings.get('storage_access_key')
        secret_key: str = settings.get('storage_secret_key')
        obj = cls(access_key, secret_key, bucket, region)
        return obj

    def _get_client(self):
        if self._client is None:
            config = Config(
                region_name=self._region,
            )
            self._client = boto3.client('s3', config=config,
                              aws_access_key_id=self._access_key,
                              aws_secret_access_key=self._secret_key)

    def download(self, filename: str, filepath: str) -> None:
        self._get_client()
        with open(filepath, "wb") as f:
            self._client.download_fileobj(
                self._bucket,
                filename,
                f
            )

    def upload(self, filename: str) -> None:
        object_name = os.path.basename(filename)
        self._get_client()
        try:
            self._client.upload_file(filename, self._bucket, object_name)
        except ClientError as e:
            raise StorageUploadException

    def delete(self, filename: str) -> None:
        self._get_client()
        try:
            self._client.delete_object(Bucket=self._bucket, Key=filename)
        except ClientError as e:
            raise StorageDeleteException
