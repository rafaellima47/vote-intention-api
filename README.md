# Desafio Python - Vote Intetion API

API simples para coleta e consulta de intenções de voto.

## Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy Async com SQLite
- Pipenv
- Pytest

## Setup local

1. Instale as dependências:

```bash
pipenv install --dev
```

2. Execute a API:

```bash
pipenv run uvicorn app.main:app --reload
```

## Executando os testes

```bash
pipenv run pytest -q
```

## Executando com Docker

1. Build da imagem:

```bash
docker build -t vote-intention-api .
```

2. Suba o container:

```bash
docker run --rm -p 8000:8000 vote-intention-api
```

## Acesse a doc em:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### GET /candidatos
Retorna a lista de candidatos.

### POST /votos
Registra uma intencao de voto.

Exemplo de payload:

```json
{
  "cpf": "12345678901",
  "candidato_id": 1
}
```

### GET /resultados
Retorna total de votos e percentual por candidato.

## Exemplos com curl

### Listar candidatos

```bash
curl -X GET "http://127.0.0.1:8000/candidatos"
```

### Registrar voto

```bash
curl -X POST "http://127.0.0.1:8000/votos" \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901","candidato_id":1}'
```

### Consultar resultados

```bash
curl -X GET "http://127.0.0.1:8000/resultados"
```
