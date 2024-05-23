output "arn" {
  value = aws_lambda_function.my_lambda.arn
}

output "name" {
  value = aws_lambda_function.my_lambda.function_name
}
