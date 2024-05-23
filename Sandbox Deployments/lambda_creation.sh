ACCOUNT_ID=$(aws sts get-caller-identity --profile $1 --query Account | tr -d '"') 
echo $ACCOUNT_ID

aws lambda create-function \
--function-name deepracer-ec2-usage-monitor \
--runtime python3.9 \
--role arn:aws:iam::${ACCOUNT_ID}:role/deepracer-ec2-usage-monitor-role \
--handler lambda_handler \
--zip-file fileb://C:/Users/abhij/Downloads/deepracer-ec2-usage-monitor.zip \
--timeout 10 \
--profile $1

aws lambda add-permission \
--function-name deepracer-ec2-usage-monitor \
--action lambda:InvokeFunction \
--statement-id event-rule \
--principal events.amazonaws.com \
--profile $1

aws events put-rule \
--name deepracer-ec2-usage-monitor \
--schedule-expression "cron(0 10 * * ? *)" \
--profile $1

aws events put-targets \
--rule deepracer-ec2-usage-monitor \
--targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:${ACCOUNT_ID}:function:deepracer-ec2-usage-monitor" \
--profile $1