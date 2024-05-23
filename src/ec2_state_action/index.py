import logging
import boto3
import datetime
import os
try:
    from src.util import logger_util
except ImportError:
    from util import logger_util

log = logger_util.get_logger('state_update', logging.INFO)

CUTOFF_SECONDS = os.environ.get('CUTOFF_SECONDS', 60 * 60 * 8)


def handler(event, context=None):
    log.info("Input event")
    log.info(event)
    table_name = os.environ.get('DYNAMO_TABLE')
    dynamodb_client = boto3.client(
        'dynamodb')

    results = []
    terminated = []
    last_evaluated_key = None
    while True:
        if last_evaluated_key:
            response = dynamodb_client.scan(
                TableName=table_name,
                ExclusiveStartKey=last_evaluated_key
            )
        else:
            response = dynamodb_client.scan(TableName=table_name)
        last_evaluated_key = response.get('LastEvaluatedKey')

        results.extend(response['Items'])

        if not last_evaluated_key:
            break
    for res in results:
        then = datetime.datetime.strptime(
            res['timestamp']['S'], "%m/%d/%Y, %H:%M:%S")
        diff = datetime.datetime.now() - then
        if diff.total_seconds() >= float(CUTOFF_SECONDS):
            log.info('instance is running for longer than 8 hours')
            log.info(diff.total_seconds())
            # TODO: Notify stakeholders
            ec2 = boto3.client('ec2')
            res = ec2.terminate_instances(
                InstanceIds=[
                    res['id']['S'],
                ]
            )
            terminated.append(res)
    return terminated
