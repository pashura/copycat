import requests

from copy_cat.services.ssm_service import SSMService

CONNECT_TIMEOUT_SEC = 60
READ_TIMEOUT_SEC = 60


class ParcelService:
    __urls = {
        "local": "https://parcel.api.spsprod.in/v3/parcels",
        "test": "https://parcel.api.spsprod.in/v3/parcels",
        "preprod": "https://parcel.api.spspreprod.in/v3/parcels",
        "prod": "https://parcel.api.spsprod.in/v3/parcels",
    }
    __Token = None

    def __init__(self, environment="test"):
        self.environment = environment
        self.url = self.__urls[environment]

    @property
    def __token(self):
        if self.__Token is None:
            ssm = SSMService()
            self.environment = (
                self.environment if self.environment in ["preprod", "prod"] else "prod"
            )
            self.__Token = ssm.get_secret(
                f"/tpd/webxd/xd-server/{self.environment}/identity.token"
            )
        return self.__Token

    def get_parcel_data(self, uid):
        headers = {"Authorization": "Bearer " + self.__token}
        url = f"{self.url}/{uid}/data"
        resp = requests.get(
            url,
            headers=headers,
            timeout=(CONNECT_TIMEOUT_SEC, READ_TIMEOUT_SEC),
            stream=True,
        )
        if resp.status_code == 200:
            return resp.content
        raise Exception(f"Unable to retrieve file by '{uid}' parcel uid.")
