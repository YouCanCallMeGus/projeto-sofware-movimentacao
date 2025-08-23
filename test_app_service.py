from app_service import validar_campos, calcular_valor, criar_objeto_movimentacao
from unittest.mock import MagicMock, patch
import requests

def test_validar_campos_completos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) is None

def test_validar_campo_ausente():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4"
    }
    assert validar_campos(data) == "Campo obrigatório 'quantidade' não informado"

@patch("app_service.requests.get")
def test_calcular_valor(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"lastValue": 40}

    mock_get.return_value = mock_response

    assert calcular_valor("PETR4", 5) == (200, None)

@patch("app_service.requests.get")
def test_calcular_valor_erro(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_get.return_value = mock_response

    ticker = "PETR4"

    assert calcular_valor(ticker, 5) == (None,f"Erro ao buscar ticker '{ticker}'")

@patch("app_service.requests.get")
def test_calcular_valor_erro_conexao(mock_get):
    mock_response = MagicMock()
    mock_response.side_effect = requests.RequestException("Invalid input")
    mock_get.side_effect = mock_response
    ticker = "PETR4"

    assert calcular_valor(ticker, 5) == (None, f"Erro de conexão: Invalid input")

def test_criar_objeto_movimentacao():
    data_response = {
        "cpf_comprador": "12312312312", 
        "cpf_vendedor": "12312312312", 
        "ticker": "PETR4", 
        "quantidade": 2, 
        "valor_movimentacao": 10
    }

    assert criar_objeto_movimentacao({"cpf_comprador": "12312312312", 
        "cpf_vendedor": "12312312312", 
        "ticker": "PETR4", 
        "quantidade": 2,}, 10) == data_response
