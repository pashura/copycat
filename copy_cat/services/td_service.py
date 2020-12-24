import requests
import urllib3

from copy_cat.exceptions import NotFoundError, ServiceError
from copy_cat.services.ssm_service import SSMSecrets

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TDService:
    __urls = {
        'local': 'https://design-ui-api.test.spsapps.net',
        'test': 'https://design-ui-api.test.spsapps.net',
        'prod': 'https://design-ui-api.spsapps.net',
    }
    __Token = None

    def __init__(self, environment='test'):
        self.environment = environment
        self.url = self.__urls[environment]

    @property
    def __token(self):
        if self.__Token is None:
            self.__Token = SSMSecrets(self.environment).get_key("identity.token")
        return self.__Token

    def get_blank_design(self, file_type: str, version: str, file_name: str) -> dict:
        try:
            rsp = requests.get(
                f'{self.url}/master_templates/XSD/{file_type}/{version}/{file_name}.json',
                verify=False, headers={'Authorization': 'Bearer ' + self.__token},
            )
        except requests.exceptions.RequestException as e:
            raise ServiceError from e

        rsp = self._process_response(rsp)
        return rsp.json()

    def search_design(self, file_name: str) -> dict:
        try:
            rsp = requests.get(
                f'{self.url}/customer_design_search/{file_name}.json',
                verify=False, headers={'Authorization': 'Bearer ' + self.__token}
            )
        except requests.exceptions.RequestException as e:
            raise ServiceError from e

        rsp = self._process_response(rsp)
        return rsp.json()

    def get_design(self, org_id: str, file_name: str):
        try:
            rsp = requests.get(
                f'{self.url}/company_designs/Companies/{org_id}/Designs/{file_name}.json',
                verify=False, headers={'Authorization': 'Bearer ' + self.__token}
            )
        except requests.exceptions.RequestException as e:
            raise ServiceError from e

        rsp = self._process_response(rsp)
        return rsp.json()

    def get_reversed_design(self, org_id: str, file_name: str):
        try:
            rsp = requests.get(
                f'{self.url}/company_designs/Companies/{org_id}/Designs/{file_name}.json/reversed',
                verify=False, headers={'Authorization': 'Bearer ' + self.__token}
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
