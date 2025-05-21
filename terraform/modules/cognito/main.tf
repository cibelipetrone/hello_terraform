resource "aws_cognito_user_pool" "main" {
  name = var.user_pool_name
  
  # Políticas de senha
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }
  
  # Configuração de verificação por email
  auto_verified_attributes = ["email"]
  
  # Configuração do esquema de atributos
  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }
  
  # Configurações de mensagens
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }
  
  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject        = "Seu código de verificação"
    email_message        = "Seu código de verificação é {####}"
  }
  
  # Configurações de recuperação de conta
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }
  
  tags = var.tags
}

# Cliente do User Pool para integração com API Gateway
resource "aws_cognito_user_pool_client" "client" {
  name                = "${var.user_pool_name}-client"
  user_pool_id        = aws_cognito_user_pool.main.id
  
  # Sem segredo de cliente para aplicações SPA/mobile
  generate_secret     = false
  
  # Configurações de autenticação - mantenha apenas os fluxos explícitos
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]

  # Configurações de tokens
  refresh_token_validity = 30
  access_token_validity  = 1
  id_token_validity      = 1
  token_validity_units {
    access_token  = "hours"
    id_token      = "hours"
    refresh_token = "days"
  }
}