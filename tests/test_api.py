from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_get_candidates(database_path: Path) -> None:
    with TestClient(app) as client:
        response = client.get("/candidatos")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "nome": "Maria Silva", "numero": 13},
        {"id": 2, "nome": "João Souza", "numero": 45},
    ]


def test_register_vote_success_and_duplicate(database_path: Path) -> None:
    with TestClient(app) as client:
        first_vote = client.post("/votos", json={"cpf": "12345678901", "candidato_id": 1})
        duplicate_vote = client.post("/votos", json={"cpf": "12345678901", "candidato_id": 2})

    assert first_vote.status_code == 201
    assert first_vote.json() == {"mensagem": "Voto registrado com sucesso"}
    assert duplicate_vote.status_code == 409
    assert duplicate_vote.json() == {"detail": "CPF já registrou um voto"}


def test_register_vote_with_invalid_cpf(database_path: Path) -> None:
    with TestClient(app) as client:
        response = client.post("/votos", json={"cpf": "123", "candidato_id": 1})

    assert response.status_code == 400
    assert response.json() == {
        "detail": "CPF deve conter exatamente 11 dígitos numéricos"
    }


def test_register_vote_with_invalid_candidate(database_path: Path) -> None:
    with TestClient(app) as client:
        response = client.post("/votos", json={"cpf": "12345678901", "candidato_id": 99})

    assert response.status_code == 400
    assert response.json() == {"detail": "candidato_id inválido"}


def test_get_results(database_path: Path) -> None:
    with TestClient(app) as client:
        client.post("/votos", json={"cpf": "12345678901", "candidato_id": 1})
        client.post("/votos", json={"cpf": "10987654321", "candidato_id": 1})
        client.post("/votos", json={"cpf": "11111111111", "candidato_id": 2})
        response = client.get("/resultados")

    assert response.status_code == 200
    assert response.json() == {
        "total_votos": 3,
        "candidatos": [
            {"id": 1, "nome": "Maria Silva", "votos": 2, "percentual": 66.67},
            {"id": 2, "nome": "João Souza", "votos": 1, "percentual": 33.33},
        ],
    }
