import requests
import urllib3

from copy_cat.common.exceptions import NotFoundError, ServiceError
from copy_cat.services.ssm_service import SSMService

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CAService:
    __urls = {
        "local": "https://company-aggregator-api.spstest.in",
        "test": "https://company-aggregator-api.spstest.in",
        "prod": "https://company-aggregator-api.spsprod.in",
    }
    __Token = None

    def __init__(self, environment="test"):
        self.environment = environment
        self.url = self.__urls[environment]

    @property
    def __token(self):
        if self.__Token is None:
            ssm = SSMService()
            self.__Token = ssm.get_secret(
                f"/tpd/jenkins/xtencil-to-design/{self.environment}/identity.token"
            )
        return self.__Token

    def get_hub_uid(self, org_id: str):
        try:
            rsp = requests.post(
                f"{self.url}/graphql",
                headers={"Authorization": "Bearer " + self.__token},
                json={"query": "{account(orgId: " + org_id + ") {Hub_ID__c}}"},
            )
        except requests.exceptions.RequestException as e:
            raise ServiceError from e

        rsp = self._process_response(rsp)
        account = rsp.json().get("data", {}).get("account")

        if not account or not account.get("Hub_ID__c"):
            return ""

        return account.get("Hub_ID__c")

    @classmethod
    def _process_response(cls, response):
        if response.status_code == 200:
            return response
        elif response.status_code == 404:
            body = response.json()
            raise NotFoundError(message=body["error"])
        else:
            raise ServiceError(status_code=response.status_code, body=response.content)
