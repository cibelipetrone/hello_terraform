output "table_name" {
  value = aws_dynamodb_table.shopping_list.name
}

output "table_arn" {
  value = aws_dynamodb_table.shopping_list.arn
}
