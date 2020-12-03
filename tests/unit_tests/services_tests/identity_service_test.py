import pytest
import requests
import requests_mock

from copy_cat.exceptions import ServiceError
from copy_cat.services.identity_service import IdentityService

identity_service = IdentityService()
IDENTITY_URL = identity_service.url + '/identity/'


def test_get_identity_token_success():
    with requests_mock.mock() as mock_:
        mock_.post(f"{IDENTITY_URL}token/", json={'token': '123'}, status_code=200)
        content = identity_service.get_identity_token()
        assert content['token'] == '123'


def test_get_identity_token_service_error():
    with requests_mock.mock() as mock_:
        mock_.post(f"{IDENTITY_URL}token/", exc=requests.exceptions.RequestException)
        with pytest.raises(ServiceError):
            identity_service.get_identity_token()


def test_get_identity_token_error():
    with requests_mock.mock() as mock_:
        mock_.post(f"{IDENTITY_URL}token/", status_code=500)
        with pytest.raises(ServiceError):
            identity_service.get_identity_token()
