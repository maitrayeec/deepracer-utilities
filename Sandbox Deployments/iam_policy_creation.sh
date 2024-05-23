ACCOUNT_ID=$(aws sts get-caller-identity --profile $1 --query Account | tr -d '"') 
echo $ACCOUNT_ID

aws iam create-role --role-name deepracer-ec2-usage-monitor-role --assume-role-policy-document \
'{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}' --profile $1

aws iam create-policy --policy-name deepracer-ec2-usage-monitor-policy --policy-document \
'{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Start*",
                "ec2:Stop*",
                "ec2:DescribeInstances*",
                "dynamodb:GetItem*",
                "dynamodb:PutItem*"
            ],
            "Resource": "*"
        }
    ]
}' --profile $1


aws iam attach-role-policy --policy-arn arn:aws:iam::${ACCOUNT_ID}:policy/deepracer-ec2-usage-monitor-policy --role-name deepracer-ec2-usage-monitor-role --profile $1