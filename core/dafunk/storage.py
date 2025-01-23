from core.dafunk.storages.s3 import S3Storage


class DaObjectStorage(object):

    @classmethod
    def from_settings(cls, settings: dict):
        storage_type = settings.get('storage')
        client = None
        if storage_type == 's3':
            client = S3Storage.from_settings(settings)
        else:
            raise NotImplementedError
        return client
