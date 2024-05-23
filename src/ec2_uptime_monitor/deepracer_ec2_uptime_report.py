import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime as dt


region = 'us-east-1'
mntrTbl = 'deepracer_ec2_uptime_monitor'
teamNmLkupTbl = 'deepracer_team_lkup'


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


def updateDynamoMonitor():
    dynamodbResource = boto3.resource('dynamodb', region_name=region)
    table = dynamodbResource.Table(mntrTbl)

    response = table.scan(FilterExpression=Attr(
        "instance_strt_tstmp").begins_with(str(dt.now().date())))
    for items in response['Items']:
        end_tstmp = str(items['instance_end_tstmp']) if len(
            str(items['instance_end_tstmp'].strip())) > 0 else str(dt.now())
        print("Instance Start Time:", items['instance_strt_tstmp'])
        print("Instance End Time:", items['instance_end_tstmp'])
        datediff = dt.strptime(end_tstmp, '%Y-%m-%d %H:%M:%S.%f') - \
            dt.strptime(items['instance_strt_tstmp'], '%Y-%m-%d %H:%M:%S.%f')

        responseUpdt = table.update_item(Key={'instance_strt_tstmp': str(items['instance_strt_tstmp']),
                                              'team_name': str(items['team_name'])},
                                         UpdateExpression="set uptime_hrs = :uptime",
                                         ExpressionAttributeValues={':uptime': str(
                                             "{:.2f}".format(datediff.total_seconds() / 3600)), },
                                         ReturnValues="UPDATED_NEW")
        print(responseUpdt)


def updateDailyHrs():

    dynamodbResource = boto3.resource('dynamodb', region_name=region)
    tblMntr = dynamodbResource.Table(mntrTbl)
    tblRpt = dynamodbResource.Table(teamNmLkupTbl)

    respsLkup = tblRpt.scan()
    for items in respsLkup['Items']:
        hrs = 0
        respsMntr = tblMntr.scan(FilterExpression=Attr("instance_strt_tstmp").begins_with(
            str(dt.now().date())) & Attr("team_name").eq(items["team_name"]))

        for itemsMntr in respsMntr['Items']:
            hrs = hrs + float(itemsMntr["uptime_hrs"])

        responseUpdt = tblRpt.update_item(Key={'team_name': str(items['team_name'])},
                                          UpdateExpression="set uptime_total_hrs = :uptime",
                                          ExpressionAttributeValues={
                                              ':uptime': str("{:.2f}".format(hrs)), },
                                          ReturnValues="UPDATED_NEW")
        print(responseUpdt)


def publishRpt(account_id):
    dynamodbResource = boto3.resource('dynamodb', region_name=region)
    tblRpt = dynamodbResource.Table(teamNmLkupTbl)
    msg = "Please find EC2 uptime report for {0}:\n\n".format(
        dt.now().date()) + "Team Name " + " Uptime Total [Hrs]\n\n"
    resposne = tblRpt.scan()
    for items in resposne['Items']:
        msg = msg + str(items["team_name"]) + " --> " + \
            str(items["uptime_total_hrs"]) + "\n"
    # print(msg)
    publish_to_sns(
        account_id, subj="Deepracer Ec2 Uptime Report - {0}".format(dt.now().date()), msg=msg)


def lambda_handler(event, context):

    accountId = context.invoked_function_arn.split(":")[4]
    print("Updating DynamoDB table for Uptime for each run of the instance")
    updateDynamoMonitor()

    print("Updating DynamoDB table for total Uptime for current day")
    updateDailyHrs()

    print("Publish report for current day")
    publishRpt(accountId)
