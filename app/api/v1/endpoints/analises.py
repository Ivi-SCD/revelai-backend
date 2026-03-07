from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.analises import AnaliseRequest, AnaliseResponse
from app.services.analises import AnaliseService

router = APIRouter(prefix="/analises", tags=["Análise de Contratação"])

_svc = AnaliseService()


@router.post("/", response_model=AnaliseResponse)
async def gerar_analise(req: AnaliseRequest):
    """
    Gera uma nova análise do cliente a partir de documentos e reuniões.
    Utiliza IA (LangChain + Groq) para processar.
    """
    try:
        return await _svc.gerar_analise(req.id_cliente, req.id_produto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{id_analise}", response_model=AnaliseResponse)
async def obter_analise(id_analise: str):
    try:
        return await _svc.obter_analise(id_analise)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/cliente/{id_cliente}/produto/{id_produto}/ultima",
    response_model=AnaliseResponse,
)
async def obter_ultima_analise(id_cliente: str, id_produto: str):
    try:
        return await _svc.obter_ultima_analise(id_cliente, id_produto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/cliente/{id_cliente}", response_model=list[AnaliseResponse])
async def listar_analises_cliente(id_cliente: str):
    return await _svc.listar_por_cliente(id_cliente)
