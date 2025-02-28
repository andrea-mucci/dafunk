import os
import secrets

from auth.requests import PermissionsRequest
from core.dafunk import Protocol, Request
from models import User, Permissions
from auth.service import service
service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    @service.route("/key/generate",
                   request=Request.POST,
                   protocol=Protocol.WEB
                   )
    async def key_generate(permissions: list[PermissionsRequest]):
        session = service.db.get_session()
        key = secrets.token_urlsafe(16)
        key_obj = User(key=key)
        session.add(key_obj)
        for permission in permissions:
            perm = Permissions(
                user=key_obj,
                name=permission.name,
                value=permission.value
            )
            session.add(perm)
        session.commit()
        session.close()

        return {"key": key}

    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()