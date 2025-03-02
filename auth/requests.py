from typing import List

from pydantic import BaseModel

class PermissionsRequest(BaseModel):
    scope: str
    value: int

class PackageRequest(BaseModel):
    name: str
    permissions: List[PermissionsRequest] | None = None