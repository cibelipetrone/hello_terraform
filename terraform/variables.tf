variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "sa-east-1" 
}

# Role IAM
variable "role_name" {
  description = "Nome da role IAM para Lambda"
  type        = string
  default     = "my_lambda_role"
}


# Lambda: hello_terraform
variable "lambda_hello_name" {
  description = "Nome da função Lambda hello_terraform"
  type        = string
  default     = "hello_terraform_lambda"
}

variable "lambda_hello_handler" {
  description = "Handler da função Lambda hello_terraform"
  type        = string
  default     = "hello_terraform.lambda_handler"
}

variable "lambda_hello_zip_path" {
  description = "Caminho para o arquivo zip da Lambda hello_terraform"
  type        = string
  default     = "../build/hello_terraform.zip"
}

# Lambda: add_item_dynamodb
variable "lambda_add_item_name" {
  description = "Nome da função Lambda add_item_dynamodb"
  type        = string
  default     = "add_item_lambda"
}

variable "lambda_add_item_handler" {
  description = "Handler da função Lambda add_item_dynamodb"
  type        = string
  default     = "add_item_dynamodb.lambda_handler"
}

variable "lambda_add_item_zip_path" {
  description = "Caminho para o arquivo zip da Lambda add_item_dynamodb"
  type        = string
  default     = "../build/add_item_dynamodb.zip"
}

# Lambda: update_item
variable "lambda_update_item_name" {
  description = "Nome da função Lambda update_item"
  type        = string
  default     = "update_item_lambda"
}

variable "lambda_update_item_handler" {
  description = "Handler da função Lambda update_item"
  type        = string
  default     = "update_item.lambda_handler"
}

variable "lambda_update_item_zip_path" {
  description = "Caminho para o arquivo zip da Lambda update_item"
  type        = string
  default     = "../build/update_item.zip"
}

# Lambda: delete_item
variable "lambda_delete_item_name" {
  description = "Nome da função Lambda delete_item"
  type        = string
  default     = "delete_item_lambda"
}

variable "lambda_delete_item_handler" {
  description = "Handler da função Lambda delete_item"
  type        = string
  default     = "delete_item.lambda_handler"
}

variable "lambda_delete_item_zip_path" {
  description = "Caminho para o arquivo zip da Lambda delete_item"
  type        = string
  default     = "../build/delete_item.zip"
}

# Runtime compartilhado entre as funções
variable "lambda_runtime" {
  description = "Runtime da Lambda"
  type        = string
  default     = "python3.9"
}

# DynamoDB
variable "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
  default     = "shopping_list"
}

# Tags
variable "tags" {
  description = "Tags para recursos AWS"
  type        = map(string)
  default     = {}
}
