import os

from dafunk import Settings
from dafunk.service import Service

service_path = os.path.dirname(os.path.abspath(__file__))
settings_file = os.path.join(service_path, "settings.yaml")
object_settings = Settings.load_from_file(settings_file)
service = Service(object_settings)