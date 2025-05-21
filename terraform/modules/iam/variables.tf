variable "role_name" {
  type        = string
  description = "Nome da role IAM para Lambda"
}

variable "dynamodb_table_arn" {
  type        = string
  description = "ARN da tabela DynamoDB que a Lambda vai acessar"
}

variable "cognito_user_pool_arn" {
  description = "ARN do User Pool do Cognito"
  type        = string
  default     = ""
}

