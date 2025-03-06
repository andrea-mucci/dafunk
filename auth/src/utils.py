from datetime import datetime, timezone, timedelta
import os
import jwt
from jwt import InvalidTokenError

from auth.src.exceptions import AuthException

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TIME_DELTA = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=TIME_DELTA)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise AuthException("Invalid token")
        return email
    except InvalidTokenError:
        raise AuthException("Invalid token")