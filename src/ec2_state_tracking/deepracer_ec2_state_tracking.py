import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime as dt


region = 'us-east-1'
teamNmLkupTbl = 'deepracer_team_lkup'
mntrTbl = 'deepracer_ec2_uptime_monitor'


def get_tag(instance_id):
    ec2Resource = boto3.resource('ec2')
    ec2instance = ec2Resource.Instance(instance_id)
    teamName = None
    for tags in ec2instance.tags:

        if tags["Key"] == 'TeamName':
            teamName = tags["Value"]
    print("Team Name Tag:", teamName)
    return teamName


def stop_instance(instance_id):

    ec2Client = boto3.client('ec2', region)
    ec2Client.stop_instances(InstanceIds=[instance_id])


def validate_team_name_tags(tag_name):
    dynamodbResource = boto3.resource('dynamodb', region_name=region)
    table = dynamodbResource.Table(teamNmLkupTbl)

    response = table.query(KeyConditionExpression=Key(
        'team_name').eq(tag_name or " "))

    if response['Items']:
        return True
    else:
        return False


def publish_to_sns(account_id, subj, msg):
    topic_arn = "arn:aws:sns:" + region + ":" + \
        account_id + ":deepracer_ec2_uptime_monitor"

    sns = boto3.client("sns")
    response = sns.publish(
        TopicArn=topic_arn,
        Message=msg,
        Subject=subj
    )
    print(response)


def updateDynamoMonitor(team_name, instance_id, operator='INSERT'):
    dynamodbResource = boto3.resource('dynamodb', region_name=region)
    table = dynamodbResource.Table(mntrTbl)
    if operator == 'INSERT':
        response = table.put_item(
            Item={
                'instance_strt_tstmp': str(dt.now()),
                'team_name': team_name,
                'instance_id': instance_id,
                'instance_end_tstmp': ' '
            }
        )
    elif operator == 'UPDATE':
        response = table.scan(FilterExpression=Attr("team_name").eq(team_name) & Attr(
            "instance_id").eq(instance_id) & Attr("instance_end_tstmp").eq(" "))

        if response['Items']:
            strt_tstmp = response['Items'][0]['instance_strt_tstmp']
            print(strt_tstmp)

            responseUpdt = table.update_item(Key={'instance_strt_tstmp': strt_tstmp, 'team_name': team_name},
                                             UpdateExpression="set instance_end_tstmp = :endt",
                                             ExpressionAttributeValues={
                                                 ':endt': str(dt.now()), },
                                             ReturnValues="UPDATED_NEW")
            print(responseUpdt)
        else:
            print("No valid instance found")


def lambda_handler(event, context):

    accountId = context.invoked_function_arn.split(":")[4]
    instanceId = event['detail']['instance-id']
    print("Instance ID: ", instanceId)
    print("Instance State: ", event['detail']['state'])
    tagName = get_tag(instanceId)

    if event['detail']['state'] == 'running':

        validate_team_name_tags(tagName)

        if tagName is None or not validate_team_name_tags(tagName):
            print("No valid tag. Stopping the Instance.")
            publish_to_sns(account_id=accountId, subj="Deepracer Ec2 Monitor",
                           msg="No valid tag found. Please add valid tag with Key: TeamName" +
                           "and Value: <repective team name>. Stopping the Instance: {0}".format(instanceId))
            stop_instance(instanceId)
        else:
            print("Instance has valid tag")
            publish_to_sns(account_id=accountId, subj="Deepracer Ec2 Monitor",
                           msg="Instance: {0} has been provisioned by the Team: {1}".format(instanceId, tagName))
            updateDynamoMonitor(team_name=tagName, instance_id=instanceId)

    elif event['detail']['state'] in ('stopping', 'shutting-down'):

        updateDynamoMonitor(team_name=tagName,
                            instance_id=instanceId, operator='UPDATE')
