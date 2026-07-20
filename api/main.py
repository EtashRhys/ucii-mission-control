from fastapi import FastAPI

from storage.database import Base
from storage.database import engine

from api.models import Event


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="UCII Mission Control",
    description="Operational observability infrastructure for UCII",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "service": "UCII Mission Control",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
