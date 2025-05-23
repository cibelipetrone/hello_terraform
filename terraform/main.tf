provider "aws" {
  region = var.aws_region
}

# Backend

terraform {
  backend "s3" {
    bucket         = "meu-terraform-state-bucket-dev"
    key            = "global/s3/terraform.tfstate"
    region         = "sa-east-1" 
    dynamodb_table = "terraform-locks-dev"
    encrypt        = true
  }
}

# Bucket para armazenar o tfstate
resource "aws_s3_bucket" "terraform_state" {
  bucket = "meu-terraform-state-bucket-dev" 

  tags = {
    Name        = "Terraform State Bucket"
    Environment = "dev"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"  
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Tabela DynamoDB para controle de locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks-dev"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform Locks Table"
    Environment = "dev"
  }
}


module "dynamodb" {
  source = "./modules/dynamodb"

  table_name = var.dynamodb_table_name
  tags       = var.tags
}

module "iam_lambda" {
  source = "./modules/iam"

  role_name             = var.role_name
  dynamodb_table_arn    = module.dynamodb.table_arn
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
  cognito_client_id    = module.cognito.client_id
}

module "lambda_add_item" {
  source = "./modules/lambda"

  function_name = var.lambda_add_item_name
  handler       = var.lambda_add_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_add_item_zip_path

  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_client_id    = module.cognito.client_id
}

module "lambda_update_item" {
  source = "./modules/lambda"

  function_name = var.lambda_update_item_name
  handler       = var.lambda_update_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_update_item_zip_path

  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_client_id    = module.cognito.client_id
}

module "lambda_delete_item" {
  source = "./modules/lambda"

  function_name = var.lambda_delete_item_name
  handler       = var.lambda_delete_item_handler
  runtime       = var.lambda_runtime
  role_arn      = module.iam_lambda.role_arn
  filename      = var.lambda_delete_item_zip_path

  cognito_user_pool_id = module.cognito.user_pool_id
  cognito_client_id    = module.cognito.client_id
}

module "api_gateway" {
  source                = "./modules/api_gateway"
  api_name              = "shopping-list-api"
  cognito_user_pool_arn = module.cognito.user_pool_arn
  lambda_hello_arn      = module.lambda_hello.lambda_arn
  lambda_hello_name     = module.lambda_hello.lambda_name
  aws_region            = var.aws_region
}