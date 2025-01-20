import base64
import os.path
import secrets
import string
import tarfile

import boto3
from botocore.config import Config


def get_s3_object(access_key: str, secret_key: str, bucket: str, key: str, s3_region: str = "eu-west-1", ) -> bytes:
    config = Config(
        region_name=s3_region
    )
    s3 = boto3.client('s3', config=config,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key)
    s3_response = s3.get_object(Bucket=bucket, Key=key)
    filecontent = s3_response['Body'].read()
    string_base_64 = base64.b64encode(filecontent)
    return string_base_64


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
