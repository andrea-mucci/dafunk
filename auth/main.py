import os

from fastapi import HTTPException
from sqlalchemy import select

from auth.src.responses import Token
from auth.src.requests import UserRequest
from auth.src.utils import create_access_token
from core.dafunk import Protocol, HttpRequest, Request
from core.dafunk.models import User
from auth.src.service import service
from core.dafunk.utils import get_password_hash, verify_password

service_path = os.path.dirname(os.path.abspath(__file__))

def main():
    @service.route("/user",
                   request=HttpRequest.POST,
                   protocol=Protocol.WEB
                   )
    async def create_user(user: UserRequest, request: Request):
        with service.db.Session() as session:
            hash_password = get_password_hash(user.password)
            user_obj = User(email=user.email, password=hash_password)
            session.add(user_obj)

            # send message to the broker
            # service.send_event("user.added", {
            #     "key": key,
            #     "package": package_obj.name,
            # })
            session.commit()
            return {"user": user_obj.id}

    @service.route("/auth/login",
                   request=HttpRequest.POST,
                   protocol=Protocol.WEB
                   )
    async def login(user: UserRequest, request: Request):
        with service.db.Session() as session:
            stmt = select(User).where(User.email == user.email)
            result = session.scalars(stmt).one_or_none()
            if result is None:
                raise HTTPException(status_code=404, detail="User not found")
            else:
                #check password
                if verify_password(user.password, result.password):
                    token = create_access_token(data={"sub": user.email})
            session.commit()
            return Token(access_token=token, token_type="bearer")

    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()