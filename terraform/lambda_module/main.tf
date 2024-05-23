data "archive_file" "archive_zip" {
  type = "zip"
  source_dir = var.path
  output_path = "${path.module}/build/${var.function_name}.zip"
}

resource "aws_lambda_function" "my_lambda" {
  function_name = var.function_name
  role = var.role_arn
  handler = var.handler
  filename = data.archive_file.archive_zip.output_path
  source_code_hash = data.archive_file.archive_zip.output_base64sha256
  runtime = var.runtime
  layers = var.layer_arns
  timeout = 360
  environment {
    variables = var.env_variables
  }
}