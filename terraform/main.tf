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
}

module "lambda_hello" {
  source = "./modules/lambda"

  function_name = var.lambda_hello_name
  handler       = var.lambda_hello_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_hello_zip_path
}

module "lambda_add_item" {
  source = "./modules/lambda"

  function_name = var.lambda_add_item_name
  handler       = var.lambda_add_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_add_item_zip_path
}

module "lambda_update_item" {
  source = "./modules/lambda"

  function_name = var.lambda_update_item_name
  handler       = var.lambda_update_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_update_item_zip_path
}

module "lambda_delete_item" {
  source = "./modules/lambda"

  function_name = var.lambda_delete_item_name
  handler       = var.lambda_delete_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_delete_item_zip_path
}