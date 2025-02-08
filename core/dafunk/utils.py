import os
import secrets
import string
import tarfile
from typing import Self

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs


def dict_keys_lower(test_dict):
    # create new dictionary with uppercase keys
    new_dict = dict(map(lambda x: (x[0].lower(), x[1]), test_dict.items()))

    # check if values are nested dictionaries and call function recursively
    for key, value in new_dict.items():
        if isinstance(value, dict):
            new_dict[key] = dict_keys_lower(value)

    return new_dict


def untar_file(filepath: str) -> None:
    directory = os.path.dirname(filepath)
    extracted_directory = os.path.join(directory, "extracted")
    os.makedirs(extracted_directory, exist_ok=True)

    if tarfile.is_tarfile(filepath):
        with tarfile.open(filepath) as tar:
            tar.extractall(os.path.join(extracted_directory))
    else:
        raise Exception(f"File {filepath} not a tar file")


def get_rand_code(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password
