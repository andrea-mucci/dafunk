import os

from auth.requests import UserRequest
from core.dafunk import Protocol, HttpRequest, Request
from core.dafunk.models import User, APIKey
from auth.service import service
from core.dafunk.utils import get_password_hash

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



    service.start(
        events_processes=False, web_processes=True
    )

if __name__ == '__main__':
    main()