import os.path
import secrets
import string
import tarfile


def get_rand_code(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def untar_file(filepath: str) -> None:
    directory = os.path.dirname(filepath)
    extracted_directory = os.path.join(directory, 'extracted')
    os.makedirs(extracted_directory, exist_ok=True)

    if tarfile.is_tarfile(filepath):
        with tarfile.open(filepath) as tar:
            tar.extractall(os.path.join(extracted_directory))
    else:
        raise Exception(f'File {filepath} not a tar file')
