from pydantic import BaseModel


class PermissionsRequest(BaseModel):
    name: str
    value: str | int