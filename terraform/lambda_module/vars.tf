variable "function_name" {
  type = string
}

variable "role_arn" {
  type = string
}

variable "handler" {
  type = string
  default = "index.handler"
}

variable "runtime" {
  type = string
}

variable "path" {
  type = string
}

variable "layer_arns" {
  type = list
}

variable "env_variables" {
  type = map(string)
}