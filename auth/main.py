import os
import secrets

from core.dafunk import Protocol, Request
from auth.service import service

service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    @service.route("/key/generate",
                   request=Request.POST,
                   protocol=Protocol.WEB
                   )
    async def key_generate():
        key = secrets.token_urlsafe(16)
        return {"key": key}

    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()