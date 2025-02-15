import asyncio
import os

from dafunk import DaSettings
from dafunk.service import DaService

service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    settings_file = os.path.join(service_path, "settings_broker.yaml")
    object_settings = DaSettings.load_from_file(settings_file)
    service = DaService(object_settings)

    @service.route("test")
    def test(message_dict: dict):
        print(message_dict['key'])
        return "ciao"

    @service.route("other_test")
    def other_test():
        return "miao"

    asyncio.run(service.start())

if __name__ == '__main__':
    main()