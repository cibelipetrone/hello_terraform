provider "aws" {
  region = var.aws_region
}


module "dynamodb" {
  source = "./modules/dynamodb"

  table_name = var.dynamodb_table_name
  tags       = var.tags
}

module "iam_lambda" {
  source = "./modules/iam"

  role_name          = var.role_name
  dynamodb_table_arn = module.dynamodb.table_arn
   cognito_user_pool_arn = module.cognito.user_pool_arn
}

module "cognito" {
  source = "./modules/cognito"

  user_pool_name = var.cognito_user_pool_name
  tags           = var.tags
}

module "lambda_hello" {
  source = "./modules/lambda"

  function_name = var.lambda_hello_name
  handler       = var.lambda_hello_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_hello_zip_path

  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_client_id = module.cognito.client_id
}

module "lambda_add_item" {
  source = "./modules/lambda"

  function_name = var.lambda_add_item_name
  handler       = var.lambda_add_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_add_item_zip_path

  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_client_id = module.cognito.client_id
}

module "lambda_update_item" {
  source = "./modules/lambda"

  function_name = var.lambda_update_item_name
  handler       = var.lambda_update_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_update_item_zip_path

  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_client_id = module.cognito.client_id
}

module "lambda_delete_item" {
  source = "./modules/lambda"

  function_name = var.lambda_delete_item_name
  handler       = var.lambda_delete_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_delete_item_zip_path

  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_client_id = module.cognito.client_id
}

module "api_gateway" {
  source                = "./modules/api_gateway"
  api_name              = "shopping-list-api"
  cognito_user_pool_arn = module.cognito.user_pool_arn
  lambda_hello_arn      = module.lambda_hello.lambda_arn
  lambda_hello_name     = module.lambda_hello.lambda_name
  aws_region            = var.aws_region
}