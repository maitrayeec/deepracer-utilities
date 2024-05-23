from unittest import mock
import pytest
import os
import boto3
from datetime import datetime, timedelta
from moto import mock_dynamodb, mock_ec2
from src.ec2_state_action.index import handler

TABLE_NAME = 'table1'
INSTANCE_ID = 'i-abcd1111'


@pytest.fixture
def data_table(ec2_instance):
    with mock_dynamodb():
        client = boto3.client("dynamodb", "us-east-1")
        client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        client.put_item(
            TableName=TABLE_NAME,
            Item={
                'id': {
                    'S': ec2_instance
                },
                'timestamp': {
                    'S': (datetime.now() - timedelta(hours=9)).strftime("%m/%d/%Y, %H:%M:%S")
                },
                'metadata': {
                    'M': {
                        'hours': {
                            'S': "1hour"
                        }
                    }
                }
            })
        client.put_item(
            TableName=TABLE_NAME,
            Item={
                'id': {
                    'S': ec2_instance + '1'
                },
                'timestamp': {
                    'S': (datetime.now() - timedelta(hours=4)).strftime("%m/%d/%Y, %H:%M:%S")
                },
                'metadata': {
                    'M': {
                        'hours': {
                            'S': "1hour"
                        }
                    }
                }
            })

        yield TABLE_NAME


@pytest.fixture
def ec2_instance():
    with mock_ec2():
        client = boto3.client("ec2", "us-east-1")
        res = client.run_instances(ImageId='ami-12c6146b', MinCount=1, MaxCount=1)
        global INSTANCE_ID
        INSTANCE_ID = res['Instances'][0]['InstanceId']
        yield INSTANCE_ID


@mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": "us-east-1", "DYNAMO_TABLE": TABLE_NAME})
def test_handler(data_table, ec2_instance):
    # test event
    res = handler({})
    assert len(res) == 1
    assert res[0]['TerminatingInstances'][0]['InstanceId'] == ec2_instance
