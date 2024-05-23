#sh ./iam_policy_creation.sh sand1
#sh ./iam_policy_creation.sh sand2
#sh ./iam_policy_creation.sh sand3
#sh ./iam_policy_creation.sh sand4
#sh ./iam_policy_creation.sh sand5
#sh ./iam_policy_creation.sh sand6
#sh ./iam_policy_creation.sh sand7
#sh ./iam_policy_creation.sh sand8
#sh ./iam_policy_creation.sh sand9
#sh ./iam_policy_creation.sh sand10
#sh ./iam_policy_creation.sh sand11
#sh ./iam_policy_creation.sh sand12


#sh ./lambda_creation.sh sand2
#sh ./lambda_creation.sh sand3
#sh ./lambda_creation.sh sand4
#sh ./lambda_creation.sh sand5
#sh ./lambda_creation.sh sand6

#sh ./dynamodb_creation.sh sand2
#sh ./dynamodb_creation.sh sand3
#sh ./dynamodb_creation.sh sand4
#sh ./dynamodb_creation.sh sand5
#sh ./dynamodb_creation.sh sand6

#Execute below after few minutes. DynamDB yet in CREATING state
sh ./dynamodb_insert.sh sand2
sh ./dynamodb_insert.sh sand3
sh ./dynamodb_insert.sh sand4
sh ./dynamodb_insert.sh sand5
sh ./dynamodb_insert.sh sand6