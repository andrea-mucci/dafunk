import podman
from podman import PodmanClient

from builder.service import service

class

@service.route("build")
def build():

    with PodmanClient() as client:
        if client.ping():
            images = client.images.list()
            for image in images:
                print(image.id)