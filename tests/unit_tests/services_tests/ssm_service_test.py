from unittest.mock import patch

from copy_cat.services.ssm_service import SSMService


class MockSSMClient:
    @staticmethod
    def get_parameter(*args, **kwargs):
        return {
            "Parameter": {
                "Name": "token",
                "Type": "string",
                "Value": "string",
                "Version": 1,
            }
        }


@patch("boto3.client")
def test_get_key_success(mock_boto_client):
    def mock_boto3_client(*args, **kwargs):
        if args[0] == "ssm":
            return MockSSMClient()

    mock_boto_client.side_effect = mock_boto3_client

    ssm_service = SSMService("test")
    response = ssm_service.get_secret("token")
    assert response == "string"
