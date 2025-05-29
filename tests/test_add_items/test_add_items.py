import json
import os

import pytest






def test_success_add_items(dynamodb_client, mock_dynamodb_table):
    os.environ["TABLE_NAME"] = mock_dynamodb_table

    from src.lambdas.shopping_list.add_item_dynamodb.add_item_dynamodb import lambda_handler

    sample_item = {
        "name": "Item 1",
        "date": "2023-10-01"
    }

    event = {
        "body": json.dumps(sample_item)
    }
    
    context = {}
    
    response = lambda_handler(event, context)

    
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["success"] is True
    assert "item" in body
    assert body["item"]["name"] == "Item 1"
    assert body["item"]["status"] == "todo"

    pk = body["item"]["PK"]
    sk = body["item"]["SK"]
    
    # Verifica se o item foi salvo no DynamoDB
    saved_item = dynamodb_client.get_item(
        TableName=mock_dynamodb_table,
        Key={
            "PK": {"S": pk},
            "SK": {"S": sk}
        }
    )
    
    assert "Item" in saved_item
    assert saved_item["Item"]["PK"]["S"] == pk
    assert saved_item["Item"]["SK"]["S"] == sk

    
def test_success_add_items(dynamodb_client, mock_dynamodb_table):
    os.environ["TABLE_NAME"] = mock_dynamodb_table

    from src.lambdas.shopping_list.add_item_dynamodb.add_item_dynamodb import lambda_handler

    sample_item = {
        "name": "Item 1",
        "date": "2023-10-01"
    }

    event = {
        "body": json.dumps(sample_item)
    }
    
    context = {}
    
    response = lambda_handler(event, context)

    
    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["success"] is True
    assert "item" in body
    assert body["item"]["name"] == "Item 1"
    assert body["item"]["status"] == "todo"

    pk = body["item"]["PK"]
    sk = body["item"]["SK"]
    
    # Verifica se o item foi salvo no DynamoDB
    saved_item = dynamodb_client.get_item(
        TableName=mock_dynamodb_table,
        Key={
            "PK": {"S": pk},
            "SK": {"S": sk}
        }
    )
    
    assert "Item" in saved_item
    assert saved_item["Item"]["PK"]["S"] == pk
    assert saved_item["Item"]["SK"]["S"] == sk


    