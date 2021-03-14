from functools import lru_cache

import boto3

from copy_cat.common.exceptions import UnknownSSMServiceError


class SSMService:
    def __init__(self, env='test', region='us-east-1'):
        self.env = env
        self.region = region

    @lru_cache(maxsize=128)
    def get_secret(self, path):
        client = boto3.client('ssm', region_name=self.region)
        response = client.get_parameter(
            Name=path,
            WithDecryption=True
        )
        if 'Parameter' in response and 'Value' in response['Parameter']:
            return response['Parameter']['Value']
        raise UnknownSSMServiceError()
