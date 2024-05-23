resource "random_id" "ident" {
  byte_length = 6
}

module "monitoring_lambdas" {
  source        = "./lambda_module"
  for_each      = local.lambda_conf
  function_name = "tooling-${each.value.function_name}-lambda${local.ident}"
  path          = "${path.module}/${each.value.path}"
  runtime       = each.value.runtime
  role_arn      = aws_iam_role.monitoring_role.arn
  layer_arns    = [aws_lambda_layer_version.lambda_layer.arn]
  handler       = each.value.handler
  depends_on    = [aws_lambda_layer_version.lambda_layer]
  env_variables = merge(tomap({
    DYNAMO_TABLE = aws_dynamodb_table.example.name ,
    }),
    each.value.env_variables
  )
}
