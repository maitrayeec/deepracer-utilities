ACCOUNT_ID=$(aws sts get-caller-identity --profile $1 --query Account | tr -d '"') 
echo $ACCOUNT_ID

aws dynamodb create-table \
--table-name deepracer_team_referencetable \
--attribute-definitions AttributeName=id,AttributeType=S \
--key-schema AttributeName=id,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
--profile $1

aws dynamodb put-item \
--table-name deepracer_team_referencetable \
--item file://dynamoitems.json \
--profile $1
