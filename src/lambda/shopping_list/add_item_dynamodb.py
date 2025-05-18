import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.client("dynamodb")
TABLE_NAME = os.getenv("TABLE_NAME", "shopping_list")


def lambda_handler(event, context):
    try:
        name = event.get("name")
        date = event.get("date")

        if not name or not date:
            return error_response(400, "'name' e 'date' são obrigatórios.")

        pk = f"list#{date.replace('-', '')}"
        sk = f"item#{uuid.uuid4()}"
        created_at = datetime.utcnow().isoformat()

        item = {
            "PK": {"S": pk},
            "SK": {"S": sk},
            "name": {"S": name},
            "status": {"S": "todo"},
            "createdAt": {"S": created_at}
        }

        dynamodb.put_item(TableName=TABLE_NAME, Item=item)

        return {
            "success": True,
            "item": simplify_item(item)
        }

    except Exception as e:
        context.logger.log(f"Erro ao salvar item: {str(e)}")
        return error_response(500, "Erro interno ao salvar item.")


def simplify_item(item):
    """Converte valores do DynamoDB para um dicionário simples Python."""
    return {k: list(v.values())[0] for k, v in item.items()}


def error_response(status_code, message):
    return {
        "success": False,
        "statusCode": status_code,
        "message": message
    }
