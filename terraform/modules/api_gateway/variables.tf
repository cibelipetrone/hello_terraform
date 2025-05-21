variable "api_name" {
  description = "Nome da API Gateway"
  type        = string
}

variable "cognito_user_pool_arn" {
  description = "ARN do Cognito User Pool"
  type        = string
}

variable "lambda_hello_arn" {
  description = "ARN da Lambda hello"
  type        = string
}

variable "lambda_hello_name" {
  description = "Nome da Lambda hello"
  type        = string
}

variable "aws_region" {
  description = "Região AWS"
  type        = string
}