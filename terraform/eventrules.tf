resource "aws_cloudwatch_event_rule" "ec2_state_rule" {
  name        = "ec2-state-rule${local.ident}"
  description = "Capture each EC2 state changes"

  event_pattern = jsonencode({
    detail-type = [
      "EC2 Instance State-change Notification"
    ]
    "source" = ["aws.ec2"]
    "detail" = {
      "state" = ["running", "terminated", "stopped", "stopping", "shutting-down", "pending"]
    }
  })
}

resource "aws_cloudwatch_event_target" "trigger_monitoring_lambda" {
  rule      = aws_cloudwatch_event_rule.ec2_state_rule.name
  target_id = "get_ec2_status"
  arn       = module.monitoring_lambdas["state_update"].arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_monitoring_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.monitoring_lambdas["state_update"].name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ec2_state_rule.arn
}

resource "aws_cloudwatch_event_rule" "every_two_hours" {
  name                = "every-two-hours${local.ident}"
  description         = "Fires every 2 hours"
  schedule_expression = "rate(120 minutes)"
}

resource "aws_cloudwatch_event_target" "trigger_action_lambda" {
  rule      = aws_cloudwatch_event_rule.every_two_hours.name
  target_id = "get_ec2_status_2_hours"
  arn       = module.monitoring_lambdas["state_action"].arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_action_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = module.monitoring_lambdas["state_action"].name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_two_hours.arn
}

