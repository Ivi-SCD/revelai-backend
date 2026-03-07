from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.uso import UsoRequest, UsoResponse
from app.services.uso import UsoService

router = APIRouter(prefix="/uso", tags=["Uso do Produto"])

_svc = UsoService()


@router.post("/gerar", response_model=UsoResponse)
async def gerar_analise_uso(req: UsoRequest):
    """
    Gera análise de uso do produto após todas as tasks estarem concluídas.
    Analisa reuniões e gera sentimentos, métricas e recomendações via IA.
    """
    try:
        return await _svc.gerar_analise_uso(req.id_cliente, req.id_produto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/cliente/{id_cliente}/produto/{id_produto}",
    response_model=UsoResponse,
)
async def obter_uso(id_cliente: str, id_produto: str):
    try:
        return await _svc.obter_uso(id_cliente, id_produto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
