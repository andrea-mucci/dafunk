import podman
from podman import PodmanClient
from pydantic import BaseModel

from builder.service import service

class Repository(BaseModel):
    name: str


@service.route("repository:update")
def build():

    with PodmanClient() as client:
        if client.ping():
            images = client.images.list()
            for image in images:
                print(image.id)