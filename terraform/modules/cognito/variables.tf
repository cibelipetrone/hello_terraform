# modules/cognito/variables.tf
variable "user_pool_name" {
  description = "Nome do User Pool do Cognito"
  type        = string
}

variable "tags" {
  description = "Tags para recursos"
  type        = map(string)
  default     = {}
}