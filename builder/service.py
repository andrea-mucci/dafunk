import os

from dafunk import DaSettings
from dafunk.service import DaService

service_path = os.path.dirname(os.path.abspath(__file__))
settings_file = os.path.join(service_path, "settings.yaml")
object_settings = DaSettings.load_from_file(settings_file)
service = DaService(object_settings)