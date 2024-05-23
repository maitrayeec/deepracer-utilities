from unittest import mock
import pytest
import os
import boto3
from datetime import datetime, timedelta
from moto import mock_dynamodb, mock_ec2
from src.ec2_state_update.index import handler

TABLE_NAME = 'table1'
INSTANCE_ID = 'i-abcd1111'


@pytest.fixture
def data_table():
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
def test_handler_ec2_start(data_table, ec2_instance):
    # test insert
    res = handler({
        "id": "7bf73129-1428-4cd3-a780-95db273d1602",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "123456789012",
        "time": "2021-11-11T21:29:54Z",
        "region": "us-east-1",
        "resources": [
            "arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"
        ],
        "detail": {
            "instance-id": ec2_instance,
            "state": "pending"
        }
    })
    assert res != {}


@mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": "us-east-1", "DYNAMO_TABLE": TABLE_NAME})
def test_handler_ec2_running(data_table, ec2_instance):

    res = handler({
        "id": "7bf73129-1428-4cd3-a780-95db273d1602",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "123456789012",
        "time": "2021-11-11T21:29:54Z",
        "region": "us-east-1",
        "resources": [
            "arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"
        ],
        "detail": {
            "instance-id": ec2_instance,
            "state": "pending"
        }
    })

    # test get
    res = handler({
        "id": "7bf73129-1428-4cd3-a780-95db273d1602",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "123456789012",
        "time": "2021-11-11T21:29:54Z",
        "region": "us-east-1",
        "resources": [
            "arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"
        ],
        "detail": {
            "instance-id": ec2_instance,
            "state": "running"
        }
    })
    assert res['Item'] != {}
    assert res['Item']['metadata']['M']['hours']['S'] == '1hour'
    assert type(datetime.strptime(
        res['Item']['timestamp']['S'], "%m/%d/%Y, %H:%M:%S")) is datetime

    dynamodb_client = boto3.client(
        'dynamodb')
    dynamodb_client.put_item(
            TableName=data_table,
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

    res = handler({
        "id": "7bf73129-1428-4cd3-a780-95db273d1602",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "123456789012",
        "time": "2021-11-11T21:29:54Z",
        "region": "us-east-1",
        "resources": [
            "arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"
        ],
        "detail": {
            "instance-id": ec2_instance,
            "state": "running"
        }
    })
    assert res['TerminatingInstances'][0]['CurrentState']['Name'] == 'shutting-down'


@mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": "us-east-1", "DYNAMO_TABLE": TABLE_NAME})
def test_handler_ec2_terminate(data_table, ec2_instance):
    # test delete
    res = handler({
        "id": "7bf73129-1428-4cd3-a780-95db273d1602",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "123456789012",
        "time": "2021-11-11T21:29:54Z",
        "region": "us-east-1",
        "resources": [
            "arn:aws:ec2:us-east-1:123456789012:instance/i-abcd1111"
        ],
        "detail": {
            "instance-id": ec2_instance,
            "state": "terminated"
        }
    })
    assert res != {}
