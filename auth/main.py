import os
from auth.src.service import service
service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    import auth.src.controllers

    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()