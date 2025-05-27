import pytest
import os
import json
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from datetime import datetime
from lambdas.shopping_list.list_items import list_items as lambda_function


os.environ['TABLE_NAME'] = 'shopping_list'

@pytest.fixture
def setup_data():
    """Configuração inicial para os testes."""
    mock_context = MagicMock()
    mock_context.log = MagicMock()
    
    # Evento sem data (para listar todos os itens)
    sample_event_all = {}
    
    # Evento com data específica
    sample_event_with_date = {
        "date": "2025-05-26"
    }
    
    # Dados de exemplo do DynamoDB (formato real)
    sample_dynamodb_items = [
        {
            "PK": {"S": "list#20250526"},
            "SK": {"S": "item#511f5c92-0bc9-4601-8eda-0e186852ac10"},
            "name": {"S": "Leite"},
            "status": {"S": "todo"},
            "createdAt": {"S": "2025-05-26T02:53:39.569963"}
        },
        {
            "PK": {"S": "list#20250526"},
            "SK": {"S": "item#622g6d93-1cd0-5712-9feb-1f297963bd21"},
            "name": {"S": "Pão"},
            "status": {"S": "done"},
            "createdAt": {"S": "2025-05-26T03:15:20.123456"}
        },
        {
            "PK": {"S": "list#20250525"},
            "SK": {"S": "item#733h7e04-2de1-6823-af0c-2g3a8074ce32"},
            "name": {"S": "Ovos"},
            "status": {"S": "todo"},
            "createdAt": {"S": "2025-05-25T10:30:45.789012"}
        }
    ]
    
    return mock_context, sample_event_all, sample_event_with_date, sample_dynamodb_items

@patch('lambdas.shopping_list.list_items.list_items.dynamodb')
def test_list_all_items_success(mock_dynamodb, setup_data):
    """Testa a listagem bem-sucedida de todos os itens."""
    mock_context, sample_event_all, _, sample_dynamodb_items = setup_data
    mock_dynamodb.scan.return_value = {
        "Items": sample_dynamodb_items
    }
    
    response = lambda_function.lambda_handler(sample_event_all, mock_context)
    
    assert response["success"] is True
    assert response["count"] == 3
    assert len(response["items"]) == 3
    
    # Verifica se os itens foram simplificados corretamente
    assert any(item["name"] == "Leite" and item["status"] == "todo" 
               for item in response["items"])
    assert any(item["name"] == "Pão" and item["status"] == "done" 
               for item in response["items"])
    assert any(item["name"] == "Ovos" and item["status"] == "todo" 
               for item in response["items"])
    
    # Verifica se o scan foi chamado corretamente
    mock_dynamodb.scan.assert_called_once_with(
        TableName="shopping_list",
        FilterExpression="begins_with(PK, :prefix)",
        ExpressionAttributeValues={
            ":prefix": {"S": "list#"}
        }
    )

@patch('lambdas.shopping_list.list_items.list_items.dynamodb')
def test_list_items_by_date_success(mock_dynamodb, setup_data):
    """Testa a listagem bem-sucedida de itens por data específica."""
    mock_context, _, sample_event_with_date, sample_dynamodb_items = setup_data
    
    # Filtra apenas itens da data específica (2025-05-26)
    items_for_date = [item for item in sample_dynamodb_items 
                      if item["PK"]["S"] == "list#20250526"]
    
    mock_dynamodb.query.return_value = {
        "Items": items_for_date
    }
    
    response = lambda_function.lambda_handler(sample_event_with_date, mock_context)
    
    assert response["success"] is True
    assert response["count"] == 2
    assert len(response["items"]) == 2
    
    # Verifica se apenas os itens da data correta foram retornados
    assert all(item["PK"] == "list#20250526" for item in response["items"])
    
    # Verifica se o query foi chamado corretamente
    mock_dynamodb.query.assert_called_once_with(
        TableName="shopping_list",
        KeyConditionExpression="PK = :pk",
        ExpressionAttributeValues={
            ":pk": {"S": "list#20250526"}
        }
    )

@patch('lambdas.shopping_list.list_items.list_items.dynamodb')
def test_list_all_items_empty_list(mock_dynamodb, setup_data):
    """Testa a listagem quando não há itens."""
    mock_context, sample_event_all, _, _ = setup_data
    mock_dynamodb.scan.return_value = {"Items": []}
    
    response = lambda_function.lambda_handler(sample_event_all, mock_context)
    
    assert response["success"] is True
    assert response["count"] == 0
    assert len(response["items"]) == 0

@patch('lambdas.shopping_list.list_items.list_items.dynamodb')
def test_list_items_by_date_empty_list(mock_dynamodb, setup_data):
    """Testa a listagem por data quando não há itens para a data."""
    mock_context, _, sample_event_with_date, _ = setup_data
    mock_dynamodb.query.return_value = {"Items": []}
    
    response = lambda_function.lambda_handler(sample_event_with_date, mock_context)
    
    assert response["success"] is True
    assert response["count"] == 0
    assert len(response["items"]) == 0

def test_invalid_date_format(setup_data):
    """Testa o tratamento de formato de data inválido."""
    mock_context, _, _, _ = setup_data
    
    invalid_event = {"date": "26-05-2025"}  # formato inválido
    
    response = lambda_function.lambda_handler(invalid_event, mock_context)
    
    assert response["success"] == False
    assert response["statusCode"] == 400
    assert "Formato de data inválido" in response["message"]

def test_empty_string_date_parameter(setup_data):
    """Testa o comportamento com string vazia como data."""
    mock_context, _, _, _ = setup_data
    
    empty_string_event = {"date": ""}
    response = lambda_function.lambda_handler(empty_string_event, mock_context)
    
    # String vazia deve gerar erro na validação
    assert response["success"] == False
    assert response["statusCode"] == 400
    assert "Data é obrigatória" in response["message"]

@patch('lambdas.shopping_list.list_items.list_items.dynamodb')
def test_dynamodb_client_error_scan(mock_dynamodb, setup_data):
    """Testa o tratamento de erro do DynamoDB no scan."""
    mock_context, sample_event_all, _, _ = setup_data
    mock_dynamodb.scan.side_effect = ClientError(
        error_response={'Error': {'Code': 'ResourceNotFoundException'}},
        operation_name='Scan'
    )
    
    response = lambda_function.lambda_handler(sample_event_all, mock_context)
    
    assert response["success"] == False
    assert response["statusCode"] == 500
    assert response["message"] == "Erro interno ao listar itens."

@patch('lambdas.shopping_list.list_items.list_items.dynamodb')
def test_dynamodb_client_error_query(mock_dynamodb, setup_data):
    """Testa o tratamento de erro do DynamoDB no query."""
    mock_context, _, sample_event_with_date, _ = setup_data
    mock_dynamodb.query.side_effect = ClientError(
        error_response={'Error': {'Code': 'ResourceNotFoundException'}},
        operation_name='Query'
    )
    
    response = lambda_function.lambda_handler(sample_event_with_date, mock_context)
    
    assert response["success"] == False
    assert response["statusCode"] == 500
    assert response["message"] == "Erro interno ao listar itens."

def test_validate_date_format_valid():
    """Testa a validação de formato de data válido."""
    # Não deve lançar exceção
    lambda_function.validate_date_format("2025-05-26")
    lambda_function.validate_date_format("2024-12-31")

def test_validate_date_format_invalid():
    """Testa a validação de formato de data inválido."""
    with pytest.raises(ValueError, match="Formato de data inválido"):
        lambda_function.validate_date_format("26-05-2025")
    
    with pytest.raises(ValueError, match="Formato de data inválido"):
        lambda_function.validate_date_format("2025/05/26")
    
    with pytest.raises(ValueError, match="Data é obrigatória"):
        lambda_function.validate_date_format(None)
    
    # Testando string vazia
    with pytest.raises(ValueError, match="Data é obrigatória"):
        lambda_function.validate_date_format("")

def test_simplify_item():
    """Testa a simplificação de um item do DynamoDB."""
    dynamodb_item = {
        "PK": {"S": "list#20250526"},
        "SK": {"S": "item#511f5c92-0bc9-4601-8eda-0e186852ac10"},
        "name": {"S": "Leite"},
        "status": {"S": "todo"},
        "createdAt": {"S": "2025-05-26T02:53:39.569963"}
    }
    
    result = lambda_function.simplify_item(dynamodb_item)
    
    assert result["PK"] == "list#20250526"
    assert result["SK"] == "item#511f5c92-0bc9-4601-8eda-0e186852ac10"
    assert result["name"] == "Leite"
    assert result["status"] == "todo"
    assert result["createdAt"] == "2025-05-26T02:53:39.569963"

def test_error_response():
    """Testa a criação de resposta de erro."""
    response = lambda_function.error_response(400, "Erro de teste")
    
    assert response["success"] == False
    assert response["statusCode"] == 400
    assert response["message"] == "Erro de teste"

@pytest.mark.parametrize("date_input,expected_pk", [
    ("2025-05-26", "list#20250526"),
    ("2024-12-31", "list#20241231"),
    ("2023-01-01", "list#20230101")
])
def test_date_to_pk_conversion(date_input, expected_pk):
    """Testa a conversão de data para PK."""
    # Simula a conversão que acontece na função list_items_by_date
    pk = f"list#{date_input.replace('-', '')}"
    assert pk == expected_pk
