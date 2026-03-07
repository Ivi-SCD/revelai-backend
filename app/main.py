from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.router import api_v1_router
from app.core.db.mongo_manager import init_database, get_mongo_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize MongoDB collections and indexes
    await init_database()
    yield
    # Shutdown: close MongoDB connection
    get_mongo_manager().close_connection()


app = FastAPI(
    title="RevelAI Backend",
    description=(
        "Plataforma de acompanhamento da jornada do cliente com IA. "
        "Cobre todo o ciclo: contratação → implantação → treinamento → uso → evolução."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_v1_router)


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
