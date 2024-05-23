## Example input
```json
[
    {
        "version": "0",
        "id": "f9964f13-170f-3c94-4edd-d7f53b0a487e",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "174862542728",
        "time": "2023-04-22T18:56:51Z",
        "region": "us-east-2",
        "resources": [
            "arn:aws:ec2:us-east-2:174862542728:instance/i-048b8029a514830f9"
        ],
        "detail": {
            "instance-id": "i-048b8029a514830f9",
            "state": "pending"
        }
    },
    {
        "version": "0",
        "id": "57427697-c6e0-e653-83e7-d34488e0203f",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "174862542728",
        "time": "2023-04-22T18:57:11Z",
        "region": "us-east-2",
        "resources": [
            "arn:aws:ec2:us-east-2:174862542728:instance/i-048b8029a514830f9"
        ],
        "detail": {
            "instance-id": "i-048b8029a514830f9",
            "state": "running"
        }
    },
    {
        "version": "0",
        "id": "53d9fabd-d4ef-2ed1-48cf-19f1b49f82dd",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "174862542728",
        "time": "2023-04-22T18:57:56Z",
        "region": "us-east-2",
        "resources": [
            "arn:aws:ec2:us-east-2:174862542728:instance/i-048b8029a514830f9"
        ],
        "detail": {
            "instance-id": "i-048b8029a514830f9",
            "state": "shutting-down"
        }
    },
    {
        "version": "0",
        "id": "c8287f0c-f0e3-c9a5-3252-c63a12ff99d3",
        "detail-type": "EC2 Instance State-change Notification",
        "source": "aws.ec2",
        "account": "174862542728",
        "time": "2023-04-22T18:58:23Z",
        "region": "us-east-2",
        "resources": [
            "arn:aws:ec2:us-east-2:174862542728:instance/i-048b8029a514830f9"
        ],
        "detail": {
            "instance-id": "i-048b8029a514830f9",
            "state": "terminated"
        }
    }
]
```