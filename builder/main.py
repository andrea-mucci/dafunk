import os

from builder.service import service

service_path = os.path.dirname(os.path.abspath(__file__))

def main():

    @service.route("test")
    def test(message_dict: dict):
        print(message_dict['key'])
        return "ciao"

    @service.route("other_test")
    def other_test():
        return "miao"

    service.start(
        events_processes=True
    )

if __name__ == '__main__':
    main()