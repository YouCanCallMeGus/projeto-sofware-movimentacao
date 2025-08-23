from unittest.mock import MagicMock, patch
from app import app, movimentacoes
import pytest

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        movimentacoes.clear()
        yield client

def test_get_movimentacoes(client):
    movimentacoes.append({
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "PETR4",
        "quantidade": 4,
        "valor_movimentacao": 124.6
    })

    response = client.get("/movimentacoes")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["ticker"] == "PETR4"


@patch("app.calcular_valor")
def test_post_movimentacao(mock_calcular_valor, client):
    mock_calcular_valor.return_value = (100.0, None)
    payload = {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "PETR4",
        "quantidade": 4
    }

    response = client.post("/movimentacoes",json=payload)
    assert response.status_code == 201

@patch("app.validar_campos")
def test_post_movimentacao_erro1(mock_validar_campos, client):
    mock_validar_campos.return_value = "Campo obrigatório não informado"
    payload = {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "PETR4"
    }
    response = client.post("/movimentacoes",json=payload)
    assert response.status_code == 400

@patch("app.calcular_valor")
def test_post_movimentacao_erro2(mock_calcular_valor, client):
    mock_calcular_valor.return_value = (None, "Erro")
    payload = {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "PETR4",
        "quantidade": 4,
    }
    response = client.post("/movimentacoes",json=payload)
    assert response.status_code == 400
