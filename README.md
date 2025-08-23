# AudiNote

## API (FastAPI)

- Run server: `uvicorn app.main:app --reload --port 8000`
- Root: `GET /` -> `{ "message": "Hello, world" }`
- Health: `GET /healthz` -> `{ "status": "ok" }`

## Tests

- Run tests: `pytest -q`
