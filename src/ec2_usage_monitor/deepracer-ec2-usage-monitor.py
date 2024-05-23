import boto3
from datetime import datetime, timezone, timedelta

region = "us-east-1"
ec2_client = boto3.client("ec2", region_name=region)
dynamodb = boto3.resource('dynamodb')
ddb_table = "deepracer_team_referencetable"
table = dynamodb.Table(ddb_table)
ddb_table_id = "deepracerdfw001"


def lambda_handler(event, context):

    ddb_response = table.get_item(Key={'id': ddb_table_id}).get("Item")
    max_hours_allowed_per_day_team = int(ddb_response.get("max_hours_per_day"))
    print("max_hours_per_day: " + str(max_hours_allowed_per_day_team))

    ec2_filters = [{
        "Name": "instance-state-name",
        "Values": ["running"],
    }
    ]
    reservations = ec2_client.describe_instances(
        Filters=ec2_filters).get("Reservations")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            launch_time = instance["LaunchTime"]
            print("Found instance_id:" + instance_id + " instance_type:" +
                  instance_type + " launch_time:" + str(launch_time))

            current_time = datetime.now(timezone.utc)
            print("Current date: " + str(current_time))
            hours_added = timedelta(hours=max_hours_allowed_per_day_team)
            max_allowed_date_and_time = launch_time + hours_added

            print("Future date: " + str(max_allowed_date_and_time))
            if (current_time > max_allowed_date_and_time):
                print(
                    "Max allowed hours exceeded, thus stopping the instance : " + instance_id)
                ec2_client.stop_instances(InstanceIds=[instance_id])
