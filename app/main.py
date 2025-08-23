from fastapi import FastAPI

app = FastAPI(title="AudiNote API")


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, world"}


@app.get("/healthz")
def healthcheck() -> dict:
    return {"status": "ok"}