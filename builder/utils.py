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
