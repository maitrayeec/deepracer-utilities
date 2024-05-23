output "iam_role_arn" {
  value = aws_iam_role.monitoring_role.arn
}

output "lambda_arns" {
  value = tomap({
    for k, lamb in module.monitoring_lambdas : k => lamb.arn
  })
}

output "dynamo_table" {
  value = aws_dynamodb_table.example.arn
}
 output "ec2_event_rule" {
  value = aws_cloudwatch_event_rule.ec2_state_rule.arn
 }