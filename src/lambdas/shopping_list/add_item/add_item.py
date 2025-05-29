import json
import logging
import os
import re
import uuid
from datetime import datetime

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client("dynamodb")
TABLE_NAME = os.getenv("TABLE_NAME", "shopping_list")


def lambda_handler(event, context):
    try:
        body = event.get("body")
        if body and isinstance(body, str):
            body = json.loads(body)
        elif not body:
            body = {}

        name = body.get("name")
        date = body.get("date")

        if not name or not date:
            return error_response(400, "'name' e 'date' são obrigatórios.")

        # Validate date format (YYYY-MM-DD)

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            return error_response(400, "Formato de data inválido. Use YYYY-MM-DD.")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return error_response(400, "Formato de data inválido. Use YYYY-MM-DD.")

        pk = f"list#{date.replace('-', '')}"
        sk = f"item#{uuid.uuid4()}"
        created_at = datetime.utcnow().isoformat()

        item = {
            "PK": {"S": pk},
            "SK": {"S": sk},
            "name": {"S": name},
            "status": {"S": "todo"},
            "createdAt": {"S": created_at},
        }

        dynamodb.put_item(TableName=TABLE_NAME, Item=item)

        response = {"success": True, "item": simplify_item(item)}

        return lambda_response(201, response)

    except Exception as e:
        logger.error(f"Erro ao salvar item: {str(e)}")
        return error_response(500, "Erro interno ao salvar item.")


def simplify_item(item):
    """Converte valores do DynamoDB para um dicionário simples Python."""
    return {k: list(v.values())[0] for k, v in item.items()}


def error_response(status_code, message):
    body = {"success": False, "message": message}

    return lambda_response(status_code, body)


def lambda_response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body_dict),
    }
