resource "aws_iam_policy" "lambda_policy" {
  name = "monitoring-role-policy${local.ident}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Action   = [
                "ec2:Start*",
                "ec2:Stop*",
                "ec2:Terminate*",
                "ec2:DescribeInstances*",
                "dynamodb:GetItem*",
                "dynamodb:PutItem*",
                "dynamodb:Scan",
                "dynamodb:DeleteItem"
            ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}


resource "aws_iam_role" "monitoring_role" {
  name                = "monitoring-role${local.ident}"
  assume_role_policy  = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = "lambdaAssume"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
  managed_policy_arns = [aws_iam_policy.lambda_policy.arn]
}

