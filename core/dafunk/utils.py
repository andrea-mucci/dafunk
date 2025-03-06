import os
import secrets
import string
import tarfile

import bcrypt


def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password.encode('utf-8'))

def get_password_hash(password) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')

def dict_keys_lower(test_dict):
    # create new dictionary with uppercase keys
    new_dict = dict(map(lambda x: (x[0].lower(), x[1]), test_dict.items()))

    # check if values are nested dictionaries and call function recursively
    for key, value in new_dict.items():
        if isinstance(value, dict):
            new_dict[key] = dict_keys_lower(value)

    return new_dict


def untar_file(filepath: str, destination_path: str = None) -> None:
    if tarfile.is_tarfile(filepath):
        with tarfile.open(filepath, 'r:gz') as tar:
            if destination_path is None:
                tar.extractall()
            else:
                tar.extract(destination_path)
    else:
        raise Exception(f"File {filepath} not a tar file")

def tar_file(filename: str, path_to_compress: str) -> None:
    with tarfile.open(filename, "w:gz") as tar:
        tar.add(path_to_compress, arcname=os.path.basename(path_to_compress))


def get_rand_code(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password
