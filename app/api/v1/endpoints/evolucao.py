from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.evolucao import EvolucaoRequest, EvolucaoResponse
from app.services.evolucao import EvolucaoService

router = APIRouter(prefix="/evolucao", tags=["Evolução do Cliente"])

_svc = EvolucaoService()


@router.post("/gerar", response_model=EvolucaoResponse)
async def gerar_evolucao(req: EvolucaoRequest):
    """
    Gera mapeamento de evolução do cliente via IA.
    Analisa uso, reuniões e análise inicial para identificar marcos e tendências.
    """
    try:
        return await _svc.gerar_evolucao(req.id_cliente, req.id_produto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/cliente/{id_cliente}/produto/{id_produto}",
    response_model=EvolucaoResponse,
)
async def obter_evolucao(id_cliente: str, id_produto: str):
    try:
        return await _svc.obter_evolucao(id_cliente, id_produto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
