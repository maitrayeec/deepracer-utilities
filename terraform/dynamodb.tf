resource "aws_dynamodb_table" "example" {
  name           = "deepracer_team_referencetable${local.ident}"
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
