ACCOUNT_ID=$(aws sts get-caller-identity --profile $1 --query Account | tr -d '"') 
echo $ACCOUNT_ID


aws dynamodb put-item \
--table-name deepracer_team_referencetable \
--item file://dynamoitems.json \
--profile $1
