import os

import requests

from copy_cat.exceptions import NotFoundError, ServiceError


class IdentityService:

    __urls = {
        'local': 'https://test.id.spsc.io',
        'test': 'https://test.id.spsc.io',
        'prod': 'https://id.spsc.io',
    }
    __Token = None

    def __init__(self, environment=os.environ.get('ENVIRONMENT', 'local')):
        self.environment = environment
        self.url = self.__urls[environment]

    @property
    def __token(self):
        # if self.__Token is None:
        #     self.__Token = SSMSecrets(self.environment).get_key("identity.token")
        return self.__Token

    def get_identity_token(self) -> dict:
        payload = {
            'grant_type': 'password',
            'username': os.environ.get('IDENTITY_USERNAME', ''),
            'password': os.environ.get('IDENTITY_PASSWORD', ''),
            'client_id': '595'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            rsp = requests.post(
                f'{self.url}/identity/token/', headers=headers,
                json=payload
            )
        except requests.exceptions.RequestException as e:
            raise ServiceError from e

        rsp = self._process_response(rsp)
        return rsp.json()

    @classmethod
    def _process_response(cls, response):
        if response.status_code == 200:
            return response
        elif response.status_code == 404:
            body = response.json()
            raise NotFoundError(message=body['error'])
        else:
            raise ServiceError(status_code=response.status_code, body=response.content)
