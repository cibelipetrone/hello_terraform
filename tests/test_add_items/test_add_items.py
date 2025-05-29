import json
import os


def test_success_add_items(dynamodb_client, mock_dynamodb_table):
    os.environ["TABLE_NAME"] = mock_dynamodb_table

    from src.lambdas.shopping_list.add_item_dynamodb.add_item_dynamodb import \
        lambda_handler

    sample_item = {"name": "Item 1", "date": "2023-10-01"}

    event = {"body": json.dumps(sample_item)}

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
        TableName=mock_dynamodb_table, Key={"PK": {"S": pk}, "SK": {"S": sk}}
    )

    assert "Item" in saved_item
    assert saved_item["Item"]["PK"]["S"] == pk
    assert saved_item["Item"]["SK"]["S"] == sk


def test_add_items_no_name_or_date(dynamodb_client, mock_dynamodb_table):
    os.environ["TABLE_NAME"] = mock_dynamodb_table

    from src.lambdas.shopping_list.add_item_dynamodb.add_item_dynamodb import \
        lambda_handler

    sample_items = [
        {"name": "", "date": "2023-10-01"},
        {"name": "item 2"},
        {"name": "item 3", "date": ""},
    ]

    responses = []

    for sample_item in sample_items:
        event = {"body": json.dumps(sample_item)}

        context = {}

        response = lambda_handler(event, context)
        body = json.loads(response["body"])
        responses.append(body)

    assert len(responses) == len(sample_items)
    for body in responses:
        assert body["success"] is False
        assert body["message"] == "'name' e 'date' são obrigatórios."


def test_add_items_invalid_date(dynamodb_client, mock_dynamodb_table):
    os.environ["TABLE_NAME"] = mock_dynamodb_table

    from src.lambdas.shopping_list.add_item_dynamodb.add_item_dynamodb import \
        lambda_handler

    sample_items = [
        {"name": "item 1", "date": "invalid-date"},
        {"name": "item 3", "date": "2023-5-01"},
        {"name": "item 4", "date": "2023-10-32"},  # Data inválida
        {"name": "item 5", "date": "2023-13-01"},  # Mês inválido
    ]

    responses = []
    for sample_item in sample_items:
        event = {"body": json.dumps(sample_item)}

        context = {}

        response = lambda_handler(event, context)
        body = json.loads(response["body"])
        responses.append(body)

    assert len(responses) == len(sample_items)
    for body in responses:
        assert body["success"] is False
        assert body["message"] == "Formato de data inválido. Use YYYY-MM-DD."
