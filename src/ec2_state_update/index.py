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

    # If state is running add to Dynamodb Table
    if event.get('detail').get('state') == 'pending':
        resp = dynamodb_client.put_item(
            TableName=table_name,
            Item={
                'id': {
                    'S': event.get('detail').get('instance-id')
                },
                'timestamp': {
                    'S': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                },
                'metadata': {
                    'M': {
                        'hours': {
                            'S': "1hour"
                        }
                    }
                }
            })
        log.info(resp)
        return resp
    # If state is terminated remove from Dynamodb Table
    if event.get('detail').get('state') in ['terminated', 'shutting-down']:
        res = dynamodb_client.delete_item(
            TableName=table_name,
            Key={
                'id': {
                    'S': event.get('detail').get('instance-id')
                }
            })
        log.info(res)
        return res
    # If state is anything else update Dynamodb
    if event.get('detail').get('state') == 'running':
        res = dynamodb_client.get_item(
            TableName=table_name,
            Key={
                'id': {
                    'S': event.get('detail').get('instance-id')
                }
            })
        then = datetime.datetime.strptime(
            res['Item']['timestamp']['S'], "%m/%d/%Y, %H:%M:%S")
        diff = datetime.datetime.now() - then
        log.info(diff.total_seconds())
        log.info(CUTOFF_SECONDS)
        if diff.total_seconds() >= float(CUTOFF_SECONDS):
            log.info('instance is running for longer than 8 hours')
            # TODO: Terminate instance
            ec2 = boto3.client('ec2')
            res = ec2.terminate_instances(
                InstanceIds=[
                    res['Item']['id']['S'],
                ]
            )
            return res
        return res
