from unittest.mock import patch

from copy_cat.services.ssm_service import SSMSecrets


class MockSSMClient:
    @staticmethod
    def get_parameters_by_path(*args, **kwargs):
        return {
            "Parameters": [
                {
                    "Name": "token",
                    "Type": "string",
                    "Value": "string",
                    "Version": 1
                }
            ]}


@patch('boto3.client')
def test_get_key_success(mock_boto_client):
    def mock_boto3_client(*args, **kwargs):
        if args[0] == 'ssm':
            return MockSSMClient()
    mock_boto_client.side_effect = mock_boto3_client

    ssm_service = SSMSecrets('test')
    response = ssm_service.get_key('token')
    assert response == 'string'


@patch('boto3.client')
def test_get_key_token_exists_success(mock_boto_client):
    def mock_boto3_client(*args, **kwargs):
        if args[0] == 'ssm':
            return MockSSMClient()
    mock_boto_client.side_effect = mock_boto3_client

    ssm_service = SSMSecrets('test')
    ssm_service.parameters = {
        "token": "token_string"
    }
    response = ssm_service.get_key('token')
    assert response == 'token_string'
