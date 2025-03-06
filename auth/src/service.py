import os
from pathlib import Path

from dafunk import Settings
from dafunk.service import Service

current_path = os.path.dirname(os.path.abspath(__file__))
path = Path(current_path)
settings_file = os.path.join(path.parent.absolute(), "settings.yaml")
object_settings = Settings.load_from_file(settings_file)
service = Service(object_settings)
