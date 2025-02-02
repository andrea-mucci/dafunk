import os
from asyncio import run

from core.dafunk import DaSettings
from core.dafunk.service import DaService

actual_path = os.path.dirname(os.path.abspath(__file__))

def main():
    settings_file = os.path.join(actual_path, "tests", "fixtures", "settings_broker.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    service = DaService(object_settings)

    @service.route("test")
    def test():
        return "ciao"

    @service.route("other_test")
    def other_test():
        return "miao"
    run(service.start())

if __name__ == '__main__':
    main()
