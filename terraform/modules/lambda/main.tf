# Configuração do AWS Cognito User Pool
resource "aws_lambda_function" "this" {
  function_name = var.function_name
  handler       = var.handler
  runtime       = var.runtime
  role          = var.role_arn
  filename      = var.filename
  source_code_hash = filebase64sha256(var.filename)

  environment {
    variables = merge(var.environment_variables, {
      COGNITO_USER_POOL_ID = var.cognito_user_pool_id
      COGNITO_CLIENT_ID    = var.cognito_client_id
      TABLE_NAME           = "shopping_list"
    })
  }
}
