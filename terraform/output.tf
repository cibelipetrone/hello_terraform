output "cognito_user_pool_id" {
  description = "ID do User Pool do Cognito"
  value       = module.cognito.user_pool_id
}

output "cognito_client_id" {
  description = "ID do Cliente do User Pool para integração com API Gateway"
  value       = module.cognito.client_id
}

output "api_invoke_url" {
  description = "URL para invocar a API"
  value       = module.api_gateway.invoke_url
}