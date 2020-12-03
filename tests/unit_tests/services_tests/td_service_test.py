import pytest
import requests
import requests_mock

from copy_cat.exceptions import NotFoundError, ServiceError
from copy_cat.services.td_service import TDService

TD = TDService('test', 'some token')
GET_BLANK_DESIGN_URL = TD.url + '/master_templates/XSD'
GET_DESIGN_URL = TD.url + '/company_designs/Companies'
SEARCH_DESIGN_URL = TD.url + '/customer_design_search'
ORGANIZATION_ID = '12345'
FILE_TYPE = 'RSX'
VERSION = '7.7'
FILE_NAME = 'Invoices'
DESIGN_NAME = 'Target_RSX_7.7_Invoices_to_X12_4010_Transaction-810'


def test_get_blank_design_success():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_BLANK_DESIGN_URL}/{FILE_TYPE}/{VERSION}/{FILE_NAME}.json', json={'design': 'design'},
                  status_code=200)
        content = TD.get_blank_design(FILE_TYPE, VERSION, FILE_NAME)
        assert content == {'design': 'design'}


def test_get_blank_design_service_error():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_BLANK_DESIGN_URL}/{FILE_TYPE}/{VERSION}/{FILE_NAME}.json',
                  exc=requests.exceptions.RequestException)
        with pytest.raises(ServiceError):
            TD.get_blank_design(FILE_TYPE, VERSION, FILE_NAME)


def test_get_blank_design_no_auth():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_BLANK_DESIGN_URL}/{FILE_TYPE}/{VERSION}/{FILE_NAME}.json',
                  json={'error': 'Not Authorized'}, status_code=404)
        with pytest.raises(NotFoundError):
            TD.get_blank_design(FILE_TYPE, VERSION, FILE_NAME)


def test_search_design_success():
    with requests_mock.mock() as mock_:
        mock_.get(f'{SEARCH_DESIGN_URL}/{FILE_NAME}.json', json={}, status_code=200)
        rsp = TD.search_design(FILE_NAME)
        assert rsp == {}


def test_search_design_error():
    with requests_mock.mock() as mock_:
        mock_.get(f'{SEARCH_DESIGN_URL}/{FILE_NAME}.json', status_code=500)
        with pytest.raises(ServiceError):
            TD.search_design(FILE_NAME)


def test_search_design_service_error():
    with requests_mock.mock() as mock_:
        mock_.get(f'{SEARCH_DESIGN_URL}/{FILE_NAME}.json', exc=requests.exceptions.RequestException)
        with pytest.raises(ServiceError):
            TD.search_design(FILE_NAME)


def test_get_design_success():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_DESIGN_URL}/{ORGANIZATION_ID}/Designs/{DESIGN_NAME}.json', json={}, status_code=200)
        rsp = TD.get_design(ORGANIZATION_ID, DESIGN_NAME)
        assert rsp == {}


def test_get_design_error():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_DESIGN_URL}/{ORGANIZATION_ID}/Designs/{DESIGN_NAME}.json', status_code=500)
        with pytest.raises(ServiceError):
            TD.get_design(ORGANIZATION_ID, DESIGN_NAME)


def test_get_design_service_error():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_DESIGN_URL}/{ORGANIZATION_ID}/Designs/{DESIGN_NAME}.json',
                  exc=requests.exceptions.RequestException)
        with pytest.raises(ServiceError):
            TD.get_design(ORGANIZATION_ID, DESIGN_NAME)


def test_get_reversed_design_success():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_DESIGN_URL}/{ORGANIZATION_ID}/Designs/{DESIGN_NAME}.json/reversed', json={}, status_code=200)
        rsp = TD.get_reversed_design(ORGANIZATION_ID, DESIGN_NAME)
        assert rsp == {}


def test_get_reversed_design_error():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_DESIGN_URL}/{ORGANIZATION_ID}/Designs/{DESIGN_NAME}.json/reversed', status_code=500)
        with pytest.raises(ServiceError):
            TD.get_reversed_design(ORGANIZATION_ID, DESIGN_NAME)


def test_get_reversed_design_service_error():
    with requests_mock.mock() as mock_:
        mock_.get(f'{GET_DESIGN_URL}/{ORGANIZATION_ID}/Designs/{DESIGN_NAME}.json/reversed',
                  exc=requests.exceptions.RequestException)
        with pytest.raises(ServiceError):
            TD.get_reversed_design(ORGANIZATION_ID, DESIGN_NAME)
