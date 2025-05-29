import os

import boto3
import pytest
from moto import mock_aws

TABLE_NAME = "testing_table"


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "sa-east-1"


@pytest.fixture
def dynamodb_client(aws_credentials):
    """Fixture to create a mocked DynamoDB client."""
    with mock_aws():
        client = boto3.client("dynamodb", region_name="sa-east-1")
        yield client


@pytest.fixture
def mock_dynamodb_table(dynamodb_client):
    """Fixture to create a mocked DynamoDB table."""

    try:
        dynamodb_client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
                {"AttributeName": "SK", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
    except dynamodb_client.exceptions.ResourceInUseException:
        # If the table already exists, we can ignore this error
        pass
    return TABLE_NAME
