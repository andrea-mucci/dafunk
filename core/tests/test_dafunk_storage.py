# #!/usr/bin/env python
#
# """Tests for `dafunk_core_library` package."""
#
# import pytest  # noqa: F401
# import os
#
# from core.dafunk import DaSettings, DaObjectStorage
# from core.dafunk.storages.s3 import S3Storage
#
# actual_path = os.path.dirname(os.path.abspath(__file__))
#
#
# def test_storage_s3(monkeypatch):
#     settings_file = os.path.join(actual_path, "fixtures", "settings_broker.yaml")
#     object_settings = DaSettings.load_from_file(settings_file)
#     storage = DaObjectStorage.from_settings(object_settings.settings)
#     assert isinstance(storage, S3Storage) == True
#
# def test_storage_s3_download(monkeypatch):
#     settings_file = os.path.join(actual_path, "fixtures", "settings_broker.yaml")
#     object_settings = DaSettings.load_from_file(settings_file)
#     storage = DaObjectStorage.from_settings(object_settings.settings)
#     download_file = os.path.join(actual_path, "fixtures", "Welcome.tar.xz")
#     storage.download("Welcome.tar.xz", download_file)
#     assert os.path.exists(download_file) == True
#     os.remove(download_file)
#
# def test_storage_s3_upload(monkeypatch):
#     settings_file = os.path.join(actual_path, "fixtures", "settings_broker.yaml")
#     object_settings = DaSettings.load_from_file(settings_file)
#     storage = DaObjectStorage.from_settings(object_settings.settings)
#     upload_file = os.path.join(actual_path, "files", "Welcome_Upload.tar.xz")
#     storage.upload(upload_file)
#     storage.delete("Welcome_Upload.tar.xz")
