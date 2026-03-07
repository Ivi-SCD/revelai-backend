from fastapi import APIRouter

from app.api.v1.endpoints.clientes import router as clientes_router
from app.api.v1.endpoints.dados import router as dados_router
from app.api.v1.endpoints.analises import router as analises_router
from app.api.v1.endpoints.implementacao import router as implementacao_router
from app.api.v1.endpoints.uso import router as uso_router
from app.api.v1.endpoints.evolucao import router as evolucao_router
from app.api.v1.endpoints.jornada import router as jornada_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(clientes_router)
api_v1_router.include_router(dados_router)
api_v1_router.include_router(analises_router)
api_v1_router.include_router(implementacao_router)
api_v1_router.include_router(uso_router)
api_v1_router.include_router(evolucao_router)
api_v1_router.include_router(jornada_router)
