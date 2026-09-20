"""Módulo de testes unitários da aplicação FastAPI."""
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from main import app, root

client = TestClient(app)

# Teste 1: Validação de status code e conteúdo da rota raiz ("/") via TestClient
def test_read_root_endpoint():
    """Valida o status code e o retorno da rota raiz /."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Teste 2: Validação direta da função assíncrona root() usando pytest-asyncio
@pytest.mark.asyncio
async def test_root_direct_async():
    """Valida a execução direta da corrotina root com await."""
    result = await root()
    assert isinstance(result, dict)
    assert result.get("message") == "Hello World"

# Teste 3: Validação da estrutura e intervalo de valores da rota "/teste1"
def test_teste1_endpoint_structure_and_range():
    """Valida formato e intervalo dos valores retornados pela rota /teste1."""
    response = client.get("/teste1")
    assert response.status_code == 200
    data = response.json()
    assert "teste" in data
    assert data["teste"] is True
    assert "num_aleatorio" in data
    assert isinstance(data["num_aleatorio"], int)
    assert 0 <= data["num_aleatorio"] <= 1000

# Teste 4: Validação determinística da função com Mock de random.randint
@patch("random.randint", return_value=42)
def test_funcaoteste_mock_random(mock_randint):
    """Valida a rota /teste1 com mock determinístico de random.randint."""
    response = client.get("/teste1")
    assert response.status_code == 200
    data = response.json()
    assert data["teste"] is True
    assert data["num_aleatorio"] == 42
    mock_randint.assert_called_once_with(0, 1000)

# Teste 5: Validação do comportamento de erro 404 para rota inexistente
def test_not_found_endpoint():
    """Valida a resposta 404 Not Found para uma rota inexistente."""
    response = client.get("/rota-inexistente")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

