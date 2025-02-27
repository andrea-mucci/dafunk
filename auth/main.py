import os
import secrets

from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from core.dafunk import Protocol, Request
from models import User
from auth.service import service
service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    @service.route("/key/generate",
                   request=Request.POST,
                   protocol=Protocol.WEB
                   )
    async def key_generate():
        session = service.db.get_session()
        key = secrets.token_urlsafe(16)
        try:
            result = session.exec(select(User).where(User.key == key)).one()
        except NoResultFound:
            key_obj = User(key=key)
            session.add(key_obj)
            session.commit()

        return {"key": key}

    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()